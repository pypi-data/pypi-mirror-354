"""
Parse XML files
"""
from typing import Any, Optional, Sequence

from lxml import etree

from ..models import Document
from ..rule import Rule
from ._parse import _prepare_context, _recursive_parse


def xml_type(
    document: Document,
    rule: Rule,
    rule_file_path: Optional[str] = None
) -> Sequence[Any] | dict[Any, Any]:
    """
    use this function if page is xml
    """

    context = etree.fromstring(document.content)

    context = _prepare_context(context, document.url)

    return _recursive_parse(context, rule, "xml", rule_file_path)
