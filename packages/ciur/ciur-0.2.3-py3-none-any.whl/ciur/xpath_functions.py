"""
Xpath function from xpath2 specification that are not supported native yet in
lxml.
This namespace is identified by the namespace fn:, which is a predefined
prefix.
This document describes implementation of function namespace
http://www.w3.org/2005/xpath-functions.

NOTE:
    local convention for all public xpath2 function is `fn_[a-z]+[a-z0-9_]+`
    is should begin with "fn_" and

    underscores `_` are converted to dash
    f.e.
        fn_string_join -> string-join(//p)

"""
from typing import Any

import re

from ciur.exceptions import CiurBaseException
from ciur.helpers import element2text, load_xpath_functions


def fn_replace(_, value: Any, pattern: str, replacement: str = "") -> str:
    """
    http://www.w3.org/TR/xpath-functions/#func-replace

    :param value: matches xpath results
    :param replacement:
    :param pattern: regex pattern
    """
    text = element2text(value)

    try:
        string = re.sub(pattern, replacement, text)
    except (re.error,) as regex_error:
        raise CiurBaseException(
            f"wrong regexp-> {regex_error} `{pattern}`"
        ) from regex_error

    return string


def fn_to_arg(_, *arg, **kwargs):
    """Conventional function which joins input as a single argument"""
    del arg, kwargs


def fn_matches(_, value, regex):
    """
    TODO: add text for this function
    The function returns true if a matches the regular expression supplied as
        $pattern as influenced by the value

    of $flags, if present; otherwise, it returns false.

    see more http://www.w3.org/TR/xpath-functions/#func-matches

    :param context: Parent DOM context
        :type context: EtreeElement
    :param value: matches xpath results
        :type value: EtreeElement or basestring
    :param regex:
        :type regex: str
    :return: return matched node
    FIXME:
    """
    text = element2text(value)

    if not text:
        return text

    try:
        match = re.search(regex, text)
    except (re.error,) as regexp_error:
        raise CiurBaseException(
            f"wrong regexp-> {regexp_error} `{regex}`"
        ) from regexp_error

    return value if match else None


def fn_string_join(context, text, separator=""):
    """
    http://www.w3.org/TR/xpath-functions/#func-string-join
    Returns a string created by concatenating the members of the
    text sequence using separator.

    :param context: Parent DOM context
        :type context: EtreeElement
    :param text: matches xpath results
        :type text: list[str]
    :param separator:
        :type separator: str
    :rtype: str
    # FIXME: deprecate this function
    """
    del context
    return separator.join(text)


def fn_upper_case(context, text):
    """
    http://www.w3.org/TR/xpath-functions/#func-upper-case
    :param context: Parent DOM context
        :type context: EtreeElement
    :param text: matches xpath results
        :type text: str

    :rtype: str
    # TODO add in documentation
    """
    del context
    return text.upper()


def fn_lower_case(context, text):
    """
    http://www.w3.org/TR/xpath-functions/#func-lower-case
    :param context: Parent DOM context
        :type context: EtreeElement
    :param text: matches xpath results
        :type text: str

    :rtype: str
    # TODO add in documentation
    """
    del context
    return text.lower()


def fn_dehumanise_number(context, number: str) -> float:
    """
    >>> fn_dehumanise_number(None,"11.5k")
    11500.0
    >>> fn_dehumanise_number(None, "69")
    69.0
    >>> fn_dehumanise_number(None, "1M")
    1000000.0
    """
    del context

    number = number.lower()
    if number[-1] == "k":
        return float(number[:-1]) * 1000
    if number[-1] == "m":
        return float(number[:-1]) * 1_000_000

    return float(number)

load_xpath_functions(locals())
