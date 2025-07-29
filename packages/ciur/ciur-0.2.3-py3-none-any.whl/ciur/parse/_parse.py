"""
parse page based on ciur rules and page type (xml, html ...)

NOTE:
    local convention for all public paring function is `[a-z]+[a-z0-9_]+_type`
    is should end with "_type"
"""
from typing import Any, Callable, Optional, Sequence, cast

import decimal
import inspect
import logging
import sys
from collections.abc import Sized

from lxml.cssselect import CSSSelector
# noinspection PyProtectedMember
from lxml.etree import XPathEvalError
from lxml.etree import _Element as EtreeElement

from ciur.exceptions import CiurBaseException
from ciur.rule import Rule

LOG = logging.getLogger(__name__)

NOT_NULL_TYPES = (bool, float, str, decimal.Decimal)
XPATH_RESULT_TYPES = Any  # pylint: disable=invalid-name


def _is_list(value: str) -> bool:
    return value.endswith("_list")


def _is_dict(value: str) -> bool:
    return value.endswith("_dict")


def _type_list_casting(
    type_list: Sequence[tuple[Callable,Sequence[str|int]]],
    res: Sequence[Any],
    url: Optional[str] = None
) -> Sequence[Any]:
    for processor, args in type_list[:-1]:
        tmp = []

        func = None
        method = None
        if isinstance(processor, (tuple, list)):
            # process class[0] + method[1] + args[2]
            method = processor[1]

        elif inspect.isfunction(processor):
            func = processor

        if func and func.__name__ == 'fn_to_arg':
            res = [res]
            continue

        for res_i in res:
            if func:
                if func.__name__.startswith("fn_"):
                    res_i = func(None, res_i, *args)
                elif func.__name__ == "url_":
                    res_i = func(res_i, url)
                else:
                    res_i = func(res_i, *args)

            if method:
                res_i = method(*(*args, res_i))

            # filter null results
            if res_i not in [None, ""]:
                tmp.append(res_i)

        res = tmp

    return res


def _evaluate_xpath(
    rule: Rule,
    context_: EtreeElement,
    doctype: str,
    rule_file_path: Optional[str] = None
) -> XPATH_RESULT_TYPES:
    selector = rule.selector

    if rule.selector_type == "xpath":
        xpath = selector
    elif rule.selector_type == "css":
        css = CSSSelector(
            selector,
            translator=doctype,
            namespaces=context_.nsmap # type: ignore[arg-type]
        )
        xpath = css.path
    else:
        raise AssertionError(
            f"unknown rule.selector_type `{rule.selector_type}`"
        )

    try:
        return context_.xpath(xpath)
    except (XPathEvalError,) as xpath_eval_error:
        raise CiurBaseException(xpath_eval_error, {
            "rule.name": rule.name,
            "rule.selector": rule.selector,
            "rule_file_path": rule_file_path
        }) from xpath_eval_error


def _shrink(res: Sequence | str | dict, is_list: bool) -> Sequence[Any] | str | dict:
    if is_list:
        return res

    if isinstance(res, list) and len(res) == 1:
        return _shrink(res[0], is_list)

    return res


def _stretch(res: XPATH_RESULT_TYPES) -> XPATH_RESULT_TYPES | Sequence[bool | float | str]:
    if isinstance(res, NOT_NULL_TYPES):
        return (res,)

    return res


def _name_colon(res: Any, name: str) -> dict[str, Any]:
    rule_name_list = name.split(":")
    if _is_list(rule_name_list[-1]):
        rule_name_list = [
            i if _is_list(i) else i + "_list" for i in rule_name_list
        ]

    return {i: res for i in rule_name_list}


def _size_match_assert(
    res: Sized,
    rule: Rule,
    url: Optional[str],
    size: Callable,
    args: Sequence[str | int]
) -> None:
    # do size match check
    try:
        size(len(res), *args)
    except (AssertionError,) as assert_error:
        raise CiurBaseException({
            "rule.name": rule.name,
            "rule.selector": rule.selector,
            "url": url
        }, f"size-match error -> {assert_error}, "
           f"on rule `{rule.name}` {args} but got {len(res)} element"
        ) from assert_error


def _resolve_parse_result(
    res: XPATH_RESULT_TYPES,
    rule: Rule,
    context_base: Optional[str]
) -> Sequence[Any] | dict:
    # filter empty items
    if not isinstance(res, (tuple, list)):
        raise ValueError(
            f'Type of `res_` must be `tuple` or `list`, {res!r}'
        )

    res2: Sequence[Any] = [i for i in res if i != ""]

    res2 = _stretch(res2)

    new_res: dict[str, EtreeElement | str | Rule ] | Sequence[Any]
    if _is_dict(rule.name):
        new_res = {
            i.pop(rule.rule[0].name): i for i in cast(list, res2)
        }
    else:
        new_res = res2

    _size_match_assert(
        # res
        new_res,
        # rule
        rule,
        # url
        context_base,
        # args ...
        *rule.type_list[-1]
    )

    new_res = _shrink(new_res, _is_list(rule.name))

    if rule.rule and (
        isinstance(new_res, NOT_NULL_TYPES) or
        new_res and isinstance(new_res, list) and
        isinstance(new_res[0], NOT_NULL_TYPES)
    ):
        sys.stderr.write("[WARN] there are children that were ignored on"
                         f" rule.name=`{rule.name}`\n")

    if isinstance(new_res, EtreeElement):
        return new_res

    if not new_res and not isinstance(new_res, NOT_NULL_TYPES):
        return tuple()

    if new_res == "":
        return tuple()

    if ":" not in rule.name:
        return {rule.name: new_res}

    return _name_colon(new_res, rule.name)


def _recursive_parse(
    context_: EtreeElement,
    rule: Rule,
    doctype: str,
    rule_file_path: Optional[str] = None
) -> Sequence[Any] | dict[Any, Any]:
    """
    recursive parse embedded rules
    """

    res = _evaluate_xpath(
        rule=rule,
        context_=context_,
        doctype=doctype,
        rule_file_path=rule_file_path
    )

    res = _stretch(res)
    res = _type_list_casting(
        type_list=rule.type_list,
        res=res,
        url=context_.base
    )

    if isinstance(res, list) and len(res) and isinstance(res[0], EtreeElement): # pylint: disable=use-implicit-booleaness-not-len
        tmp_list: XPATH_RESULT_TYPES = []
        if rule.rule:
            for res_i in res:
                tmp_ordered_dict: dict[str, Any] = {}
                for rule_i in rule.rule:
                    data = _recursive_parse(
                        res_i,
                        rule_i,
                        doctype,
                        rule_file_path=rule_file_path
                    )
                    if len(data):
                        tmp_ordered_dict.update(cast(dict, data))

                if tmp_ordered_dict:
                    tmp_list.append(tmp_ordered_dict)

            res = tmp_list

    return _resolve_parse_result(
        res=res,
        rule=rule,
        context_base=context_.base
    )


def _prepare_context(context_: EtreeElement, url: Optional[str] = None) -> EtreeElement:
    if not isinstance(context_, EtreeElement):
        context_ = context_.getroot()

    if url:
        context_.base = url

    return context_
