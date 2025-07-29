"""
This module collects helper functions and classes.
"""

from typing import Optional, cast

import inspect
import io
import sys
from pathlib import Path

import requests
from requests import Response

import ciur
from ciur import CONF, bnf_parser, get_logger, parse, pretty_json
from ciur.exceptions import CiurBaseException
from ciur.helpers import is_url
from ciur.models import Document
from ciur.rule import Rule

REQ_SESSION = requests.Session()


LOGGER = get_logger(__name__)


def _resolve_ciur_definition(
    ciur_file_or_path: io.StringIO | str,
    called_by_script: str
) -> str:
    if isinstance(ciur_file_or_path, io.StringIO):
        definition = ciur_file_or_path.read()
    else:
        ciur_file_path = ciur.path(ciur_file_or_path, called_by_script)

        definition = Path(ciur_file_path).read_bytes().decode()

    return definition


def _resolve_doc_type(doctype: Optional[str], headers: dict[str, str]) -> Optional[str]:
    if doctype:
        return doctype

    for i_doc_type in dir(parse):
        if i_doc_type.endswith("_type") and i_doc_type.replace(
            "_type", "") in headers["content-type"]:

            doctype = i_doc_type
            break
    else:
        raise CiurBaseException(
            f"can not autodetect doc_type `{headers["content-type"]}`"
        )

    return doctype


def pretty_parse(ciur_file_or_path, # pylint: disable=too-many-arguments,too-many-positional-arguments
                  url,
                  doctype=None,
                  namespace=None,
                  headers=None,
                  encoding=None,
                  req_callback=None):
    """
    WARN:
        do not use this helper in production,
        use only for sake of example,
        because of redundant rules and http session

    :param doctype: MIME types to specify the nature of the file currently
        being handled.
        see http://www.freeformatter.com/mime-types-list.html

    :param req_callback:
    :param ciur_file_or_path: external dsl
    :param url: url to be fetch with GET requests lib
    :return : extracted data as pretty json
    """
    if not headers:
        headers = ciur.HTTP_HEADERS

    ciur_definition = _resolve_ciur_definition(
        ciur_file_or_path,

        # workaround for get relative files
        inspect.stack()[1][1]
    )

    res = bnf_parser.external2dict(ciur_definition, namespace=namespace)
    rule = Rule.from_list(res)

    if req_callback:
        response = req_callback()
    else:
        response = REQ_SESSION.get(url, headers=headers)
        # TODO: set http timeout 10

    if not CONF["IGNORE_WARNING"]:
        for key in ("Etag", "Last-Modified", "Expires", "Cache-Control"):
            if response.headers.get(key):
                sys.stderr.write("[WARN] request.response has Etag, . "
                                 "TODO: link to documentation\n")

    doctype = _resolve_doc_type(doctype, dict(response.headers))

    parse_fun = getattr(parse, doctype)

    if not encoding:
        encoding = response.apparent_encoding

    data = parse_fun(ciur.models.Document(
        response.content,
        url=response.url,
        namespace=namespace,
        encoding=encoding
    ), rule[0])

    return pretty_json(data)


def pretty_parse_from_document(
    rule: io.StringIO | str,
    document: Document
) -> str:
    """
    WARN:
        do not use this helper in production,
        use only for sake of example,
        because of redundant rules and http session

    :param rule: row text for external dsl
    :param url: url to be fetch with GET requests lib
    :return : extracted data as pretty json
    """

    res = bnf_parser.external2dict(rule, namespace=document.namespace)
    rule_ = Rule.from_list(res)

    parse_fun = getattr(parse, document.doctype + "_type")

    data = parse_fun(document, rule_[0])

    return pretty_json(data)


def pretty_parse_from_resources(
    ciur_rule: str,
    document_to_parse: Response | str,
    namespace: bool = False,
    doctype: str = "/html"
) -> str:
    if is_url(ciur_rule):
        LOGGER.info("Downloading rule %r", ciur_rule)
        response = REQ_SESSION.get(ciur_rule, headers=ciur.HTTP_HEADERS)
        ciur_rule = response.text
    # else:
    #     with ciur.open_file(ciur_rule, __file__) as file_cursor:
    #         ciur_rule = file_cursor.read()

    if is_url(document_to_parse):
        document = Document.from_url(
            url=cast(str, document_to_parse),
            namespace=namespace
        )
    else:
        # with ciur.open_file(document_to_parse, __file__) as file_cursor:
        #     document_to_parse = file_cursor.read()

        document = Document(
            content=cast(Response, document_to_parse),
            namespace=namespace,
            doctype=doctype
        )

    return pretty_parse_from_document(ciur_rule, document)
