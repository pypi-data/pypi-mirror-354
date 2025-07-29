"""
place where to hold all Models related class of ``ciur``
"""
from typing import Optional

import copy

import requests
from requests.models import Response

import ciur
from ciur.helpers import is_url

LOG = ciur.get_logger(__name__)

REQ_SESSION = requests.Session()

class Document:  # pylint: disable=too-few-public-methods
    """
    Model for encapsulated data.
    Scope:
        workaround for too-many-arguments for pylint, to not pass more than
        5 argument in a functions
    """
    def __init__( # pylint: disable=too-many-arguments,too-many-positional-arguments
            self,
            content: Response | bytes,
            namespace: bool = False,
            encoding: Optional[str] = None,
            url: Optional[str] = None,
            doctype: str = "/html"
    ) -> None:
        """
        :param doctype: MIME types to specify the nature of the file currently
            being handled.
            see http://www.freeformatter.com/mime-types-list.html
        """
        self.url: Optional[str]
        self.encoding: Optional[str]

        if isinstance(content, Response):
            response: Response = content
            self.content = response.content
            self.encoding = response.apparent_encoding
            self.url = response.url
            doctype = response.headers["content-type"]
        else:
            self.content = content
            self.encoding = encoding
            self.url = url

        if doctype:
            if "/xml" in doctype:
                doctype = "xml"
            elif "/pdf" in doctype:
                doctype = "pdf"
            elif "/html" in doctype:
                doctype = "html"
        elif hasattr(content, "name"):
            if content.name.endswith(".html") or content.name.endswith(".htm"):
                doctype = "html"
            # try to add more fallback here

        self.doctype = doctype

        self.namespace = namespace

    def __str__(self):
        _ = {
            "content": self.content
        }
        if self.encoding:
            _["encoding"] = self.encoding

        if self.url:
            _["url"] = self.url

        if self.namespace:
            _["namespace"] = self.namespace

        return f"Document{_}"

    @classmethod
    def from_url(cls,
                 url: str,
                 headers: Optional[dict[str, str]] = None,
                 namespace: bool = True) -> 'Document':

        if not is_url(url):
            raise ValueError(f"Url input {url} must be a valid URL")

        if not headers:
            headers = copy.deepcopy(ciur.HTTP_HEADERS)

        LOG.info("Downloading document to parse %r", url)
        response = REQ_SESSION.get(url, headers=headers)
        return cls(response, namespace=namespace)
