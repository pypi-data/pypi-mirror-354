"""
Parse PDF files
"""
from typing import Any, Optional, Sequence

from io import BytesIO, StringIO

# pylint: disable=import-error
from pdfminer.pdfdevice import TagExtractor  # type: ignore[import-untyped]
from pdfminer.pdfinterp import (  # type: ignore[import-untyped] # pylint: disable=no-name-in-module
    PDFResourceManager, process_pdf)

# pylint: enable=import-error
from ciur.models import Document

from ..rule import Rule
from .parse_xml import xml_type


def pdf_type(
    document: Document,
    rule: Rule,
    rule_file_path: Optional[str] = None
) -> Sequence[Any] | dict[Any, Any]:
    """
    use this function if page is pdf
    """

    class MyIO(StringIO):
        encoding = "utf-8"

    resource_manager = PDFResourceManager()

    out_fp = MyIO()
    in_fp = BytesIO(document.content)

    device = TagExtractor(resource_manager, out_fp)

    process_pdf(resource_manager, device, in_fp)

    out_fp.seek(0)  # reset the buffer position to the beginning

    xml = Document(
        out_fp.read(), # type: ignore[arg-type]
        namespace=document.namespace,
        url=document.url
    )
    return xml_type(xml, rule, rule_file_path)
