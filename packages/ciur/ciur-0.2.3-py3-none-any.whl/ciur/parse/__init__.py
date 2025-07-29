"""
Parse Document: XML, HTML and PDF
"""
from ciur.models import Document

from .parse_html import html_type
from .parse_xml import xml_type

__all__ = ["html_type", "xml_type", "Document"]
