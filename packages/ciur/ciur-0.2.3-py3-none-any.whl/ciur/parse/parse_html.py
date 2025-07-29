"""
Parse HTML files
"""
from typing import Any, Optional, Sequence

import html5lib

from ..models import Document
from ..rule import Rule
from ._parse import _prepare_context, _recursive_parse


def html_type(
    document: Document,
    rule: Rule,
    rule_file_path: Optional[str] = None
) -> Sequence[Any] | dict[Any, Any]:
    """Use this function if page is HTML"""

    html = html5lib.parse(
        doc=document.content,
        treebuilder="lxml",
        namespaceHTMLElements=document.namespace,
    )

    html = _prepare_context(html, document.url)

    return _recursive_parse(
        context_=html,
        rule=rule,
        doctype="html",
        rule_file_path=rule_file_path
    )
