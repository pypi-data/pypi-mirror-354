"""
*Ciur is a scrapper layer based on DSL for extracting data*

*Ciur is a lib because it has less black magic than a framework*

If you are annoyed by `Spaghetti code` then we can taste `Lasagna code`
with the help of Ciur
"""
from typing import IO, Any, Sequence

import importlib.metadata
import json
import logging
import os
import sys
import warnings

from lxml.etree import CommentBase

from . import optional_requests

NAME = "ciur"
VERSION = importlib.metadata.version(NAME)
META = importlib.metadata.metadata(NAME)
GIT = META.get('Project-URL')


# TODO make configurable
CONF = {
    "IGNORE_WARNING":  False
}

HTTP_HEADERS = {
    "User-Agent": f"{NAME}/{VERSION} {optional_requests.DISPLAY_VERSION} {GIT}"
}


def pretty_json(data: dict[str, Any]| Sequence[dict[str, Any]]) -> str:
    """
    wrapper for long code
    :param data: to be converted in json
    :type data: object
    :return: json
    """

    def default(value):
        """
        is a function that should return a serializable version of obj or
        repr(value).

        :param value:
        :type value: object
        :rtype: str
        """

        if isinstance(value, CommentBase):
            return f"<!--{value.text} {value.tail} -->"

        return repr(value)

    res = json.dumps(data, indent=4, ensure_ascii=False, default=default)
    return res


class CommonEqualityMixin:  # pylint: disable=too-few-public-methods
    """
    boilerplate class for equal method
    """
    def __eq__(self, other):
        return isinstance(other, self.__class__) and \
            self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)


def path(relative: str, root: str = __file__) -> str:
    """
    :param relative: path
    :param root: path
    :return: absolute path
    """
    root_ = os.path.dirname(os.path.abspath(root))
    return os.path.join(root_, relative)


def open_file(relative: str, root: str = __file__, mode: str = 'r') -> IO[Any]:
    """
    :param relative: path
    :param root: path
    :param mode: file mode read, write, binary ...
    :return: absolute path
    """
    return open(path(relative, root), mode, encoding="utf-8")


def get_logger(name, formatter=None, handler=None, level=logging.INFO):
    """
    :param name: usually __name__
        :type name: str
    :param formatter: Formatter instances are used to convert a
        LogRecord to text.
        :type formatter: logging.Formatter
    :param handler: Handler instances dispatch logging events to
        specific destinations.
        :type handler: logging.Handler
    :param level: log level
        :type level: long or int
    :return: logger
        :rtype: logging.Logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    handler = handler or logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(
        formatter or
        "%(asctime)s [%(levelname)s] %(funcName)s(%(lineno)d) - %(message)s"
    ))
    logger.addHandler(handler)

    def custom_warn(message, category, filename, lineno, *_):
        """
        redirect logs from warning module to log module
        :param message:
            :type message: str
        :param category: a class that the warning must be a subclass of
            :type category: warnings.WarningMessage
        :param filename:
            :type filename: str
        :param lineno:
            :type lineno: int
        :param _: unused
        """
        if CONF["IGNORE_WARNING"]:
            return

        logger.warning(
            warnings.formatwarning(message, category, filename, lineno).strip()
        )

    warnings.showwarning = custom_warn

    return logger
