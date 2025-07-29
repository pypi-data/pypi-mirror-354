"""
ciur internal dsl (python api)
"""
from typing import Any, Callable, Literal, Optional, Sequence, cast

import builtins
import json
import re
from types import FunctionType

import ciur.xpath_functions_ciur
from ciur import bnf_parser, pretty_json

_JSON = str

_SELECTOR_TYPE_SET = {"xpath", "css"}
_SEQUENCE_TYPE = (tuple, list)

class Rule(ciur.CommonEqualityMixin):
    """
    >>> rule1 = Rule("root", "/h3", "+",
    ...  Rule("name", ".//h1[contains(., 'Justin')]/text()", "+1"),
    ...  Rule("count_list", ".//h2[contains(., 'Andrei')]/p", ["int", "+"]),
    ...  Rule("user", ".//h5[contains(., 'Andrei')]/p", "+",
    ...         Rule("name", "./spam/text()", "+1"),
    ...         Rule("sure_name", "./bold/text()", "+1"),
    ...         Rule("age", "./it", "int"),
    ...         Rule("hobby", "./li/text()", "+"),
    ...         Rule("indexes", "./li/bold", ["int", "+"])
    ...       )
    ... )

    >>> res1 = pretty_json(rule1.to_dict())
    >>> print(res1)  # doctest: +NORMALIZE_WHITESPACE
    {
        "name": "root",
        "selector": "/h3",
        "selector_type": "xpath",
        "type_list": "+",
        "rule": [
            {
                "name": "name",
                "selector": ".//h1[contains(., 'Justin')]/text()",
                "selector_type": "xpath",
                "type_list": "+1"
            },
            {
                "name": "count_list",
                "selector": ".//h2[contains(., 'Andrei')]/p",
                "selector_type": "xpath",
                "type_list": [
                    "int",
                    "+"
                ]
            },
            {
                "name": "user",
                "selector": ".//h5[contains(., 'Andrei')]/p",
                "selector_type": "xpath",
                "type_list": "+",
                "rule": [
                    {
                        "name": "name",
                        "selector": "./spam/text()",
                        "selector_type": "xpath",
                        "type_list": "+1"
                    },
                    {
                        "name": "sure_name",
                        "selector": "./bold/text()",
                        "selector_type": "xpath",
                        "type_list": "+1"
                    },
                    {
                        "name": "age",
                        "selector": "./it",
                        "selector_type": "xpath",
                        "type_list": "int"
                    },
                    {
                        "name": "hobby",
                        "selector": "./li/text()",
                        "selector_type": "xpath",
                        "type_list": "+"
                    },
                    {
                        "name": "indexes",
                        "selector": "./li/bold",
                        "selector_type": "xpath",
                        "type_list": [
                            "int",
                            "+"
                        ]
                    }
                ]
            }
        ]
    }

    >>> rule2 = Rule.from_dict(res1)
    >>> rule1.to_dict() == rule2.to_dict()
    True
    >>> rule1 == rule2
    True
    """
    rule: Sequence["Rule"]

    def __init__(self,
                 name: str,
                 selector: str,
                 type_list_: str,
                 *selector_type_and_or_rule) -> None:
        self.name = name
        self.selector = selector

        if not selector_type_and_or_rule:
            self.selector_type = "xpath"
            self.rule: Sequence[str] = tuple()
        else:
            selector_type = selector_type_and_or_rule[0]
            if isinstance(selector_type, self.__class__):
                self.selector_type = "xpath"
                self.rule = selector_type_and_or_rule
            elif selector_type in _SELECTOR_TYPE_SET:
                self.selector_type = selector_type
                self.rule = selector_type_and_or_rule[1]
            else:
                raise NotImplementedError("new Use case not Rule, css or xpath")

        # mutable object is eval !
        if isinstance(self.rule, list):
            self.rule = tuple(self.rule)

        tmp: list = []

        for type_i in self._2complex(type_list_):
            #  assert isinstance(type_i, basestring)

            func_name: str | Literal['size']

            if isinstance(type_i, (list, tuple)):
                func_name = type_i[0]
                args = type_i[1:]

            else:
                size_assert = self._assert_result_size(type_i)
                if size_assert:
                    func_name, args = size_assert
                else:
                    func_name = type_i
                    args = tuple() # type: ignore[assignment]

            self._chain_functions_to_selector(
                chain=tmp,
                func_name=func_name,
                function_args=args
            )

        self.type_list = tmp

    @classmethod
    def _assert_result_size(cls, language_token: str) -> Optional[tuple[
            Literal['size'],
            tuple[Literal['mandatory', 'optional'], int]
    ]]:
        """
        - plus (+) at least one result will be requireds
        - asterix (*) the result will be optional
        - numbers after the plus or asterix presents exact matching size

        Examples::

            +2 exact two matches will be required
            *2 nothing or two matches will be required
        """
        match = re.search(r"^([*+])(\d*)$", language_token)
        if not match:
            return None

        return "size", (
            "mandatory" if match.group(1) == "+" else "optional",
            int(match.group(2) or 0),
        )

    @classmethod
    def _chain_functions_to_selector(
        cls,
        func_name: str | Sequence[str],
        function_args: Sequence[str | int],
        chain: list[tuple[Sequence[Callable], Sequence[str | int]]]
    ):
        # TODO there are 2 entity function and methods of object,
        # TODO  rename func_name into callable_name
        if isinstance(func_name, list):
            obj_str, method_str = func_name

            obj = getattr(builtins, obj_str)
            method = str, getattr(obj, method_str)
            chain.append((method, function_args))
            return

        # func_name is str
        func_name = cast(str, func_name)
        for casting_module in bnf_parser.casting_modules:
            # TODO: test this !!!!!!
            try:
                chain.append((
                    getattr(casting_module, func_name + "_"),
                    function_args
                ))
                break
            except (AttributeError,):
                pass

            try:
                chain.append((
                    getattr(casting_module, "fn_" + func_name),
                    function_args
                ))
                break
            except (AttributeError,):
                pass

    @classmethod
    def _2complex(
        cls,
        value: Sequence[ str | Literal['size'] ] | str | Literal['size']
    ) -> Sequence[str | Literal['size']]:
        """
        convert data from simple/compact format into complex/verbose format
        :param value:
            :type value: tuple or list or str
        :rtype: tuple
        """
        if not isinstance(value, (tuple, list)):

            # noinspection PyRedundantParentheses
            return (value, ) # type: ignore[return-value]

        if isinstance(value, list):
            return tuple(value)

        return value

    @classmethod
    def _2simple_for_function_type(
        cls,
        function: Callable | Sequence[str],
        function_properties: Sequence
    ) -> Callable[..., Any] | Sequence[str]:
        if not isinstance(function, FunctionType):
            return function

        if function.__name__ == "size_":
            required = "+" if function_properties[0] == "mandatory" else "*"
            next_function = (
                "" if function_properties[1] == 0 else function_properties[1]
            )

            return f"{required}{next_function}"

        if function_properties[1]:
            return function

        if function.__name__.startswith("fn_"):
            return str(function_properties[3:])

        if function.__name__.endswith("_"):
            # TODO: debug type
            return str(function_properties[:-1])

        raise NotImplementedError(f"new use case {function=}")

    @classmethod
    def _2simple(
        cls,
        complex_verbose_format: Sequence
    ) -> Sequence[Callable| str ] | str:
        """
        convert data from complex/verbose format into simple/compact
        :param complex_verbose_format:
        :rtype: value or list or tuple
        """
        if not isinstance(complex_verbose_format, _SEQUENCE_TYPE):
            return complex_verbose_format

        simple = []
        # TODO: make a structure
        # function:
        #    name: str
        #    optional: true|false
        #    next_functions: list
        for func, func_properties in complex_verbose_format:
            tmp_i = cls._2simple_for_function_type(
                func,
                func_properties
            )

            simple.append(tmp_i)

        if len(complex_verbose_format) == 1:
            return simple[0] # type: ignore[return-value]

        ## FIXME: never is called
        return tuple(simple) # type: ignore[arg-type]

    @staticmethod
    def from_dict(input_definition: dict | str):
        """
        Factory method, build `Rule` object from `dict_`
        :param definition:
            :type definition: dict or basestring
        :rtype: Rule
        """
        definition: dict

        if isinstance(input_definition, _JSON):
            definition = json.loads(input_definition)
        else:
            definition = input_definition

        # check for children, emtpy list [] means no children
        sub_rule = tuple(list(
            Rule.from_dict(rule)
            for rule in definition.get("rule", tuple())
        ))

        type_list = definition["type_list"]
        if isinstance(type_list, list):
            type_list = tuple(type_list)

        return Rule(
            definition["name"],
            definition["selector"],
            type_list,
            *(
                definition.get("selector_type", "xpath"),
                sub_rule
            )
        )

    @staticmethod
    def from_list(list_: Sequence[dict[str, Any]]) -> 'ListOfT':
        """
        factory method, build ListOf `Rule` objects from `list_`
        :param list_:
            :type list_: list
        :rtype: list of Rule
        """
        return ListOfT(Rule.from_dict(i) for i in list_)

    @staticmethod
    def from_dsl(dsl):
        """
        factory method, build rule from dsl
        :param dsl:
            :type dsl: FileIO or str
        :rtype: list of Rule
        """
        res = bnf_parser.external2dict(dsl)

        return Rule.from_list(res)

    def to_dict(self) -> dict[str, str | Sequence[str | Callable]]:
        """
        exporting/serialising `Rule` object into dict
        """
        ret: dict[str, Any] = {
            'name': self.name,
            'selector': self.selector,
            'selector_type': self.selector_type,
            'type_list': self._2simple(self.type_list)
        }

        rule = [i.to_dict() for i in self.rule]
        if rule:
            ret["rule"] = rule

        return ret

    def __repr__(self) -> str:
        return "%s.%s(%s)" % ( # pylint: disable=consider-using-f-string
            self.__class__.__module__,
            self.__class__.__name__,
            self.to_dict()
        )

    def __str__(self) -> str:
        pretty = pretty_json(self.to_dict())
        return "%s.%s(%s)" % ( # pylint: disable=consider-using-f-string
            self.__class__.__module__,
            self.__class__.__name__,
            pretty
        )


class ListOfT(list):
    """
    wrapper for List Of Dict
    The purpose is to have pretty print option for that complex type
    """
    @classmethod
    def _callback(cls, value):
        """
        define logic of serialization
        :param value:
            :type value: object
        :rtype: value
        """
        return value

    def __str__(self) -> str:
        # pylint: disable=consider-using-f-string)
        name = "%s.%s:" % (self.__class__.__module__, self.__class__.__name__)
        res = name + "".join(
            "\n-----------%d-\n%s" % (index, self._callback(t))
            for index, t in enumerate(self, 1)
        ).replace("\n", "\n    ")

        return res


class ListOfDict(ListOfT):
    """
    wrapper for List Of Dict
    The purpose is to have a pretty print option for that complex type
    """
    @classmethod
    def _callback(cls, value) -> str:
        return pretty_json(value)
