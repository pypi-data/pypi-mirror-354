#!/usr/bin/env python
"""
Command line interface for ``ciur`` module.
"""
import argparse
import io
import logging
import platform
import sys
from argparse import RawTextHelpFormatter

import requests.exceptions
from requests.models import PreparedRequest

import ciur
from ciur.helpers import is_url
from ciur.shortcuts import pretty_parse_from_resources

LOG = logging.getLogger(__name__)


def check_url(url):
    """
    :param url:
        :type url: str
    """
    prepared_request = PreparedRequest()
    try:
        prepared_request.prepare_url(url, None)
        return prepared_request.url
    except (requests.exceptions.MissingSchema,) as url_error:
        raise argparse.ArgumentTypeError(url_error)


def check_file(path) -> io.StringIO:
    """
    :param path:
        :type path: str
    """
    if not path.endswith(".ciur"):
        sys.stderr.write("[WARN] is recommended that rule files have"
                         "extension `.ciur`\n\n")

    try:
        with open(path, mode='b+r') as f:
            the_file = io.StringIO(f.read().decode())
            the_file.name = f.name
            return the_file

    except (IOError, ) as io_error:
        raise argparse.ArgumentTypeError(io_error)


def check_resource(path: str):
    if is_url(path):
        return check_url(path)

    return check_file(path)


PARSER = argparse.ArgumentParser(
    description=ciur.__doc__,
    formatter_class=RawTextHelpFormatter,
    prog=ciur.NAME
)


PARSER.add_argument(
    "-p",
    "--parse",
    required=True,
    help="url or local file path required document for html, xml, pdf. "
         "(f.e. https://example.org or /tmp/example.org.html)",
    type=check_resource
)

PARSER.add_argument(
    "-r",
    "--rule",
    required=True,
    help="url or local file path file with parsing dsl rule "
         "(f.e. /tmp/example.org.ciur or https:/host/example.org.ciur)",
    type=check_resource
)

PARSER.add_argument(
    "-w", "--ignore_warn",
    action="store_true",
    help="suppress python warning warnings and ciur warnings hints",
)

VERSION_STRING = f"{ciur.NAME}/{ciur.VERSION} " \
                 f"Python/{platform.python_version()} " \
                 f"{platform.system()}/{platform.release()}"


PARSER.add_argument(
    '-v', '--version',
    action='version',
    version=VERSION_STRING
)


def parse_cli(*argv):
    """
    :param argv: command line arguments
    """
    args = PARSER.parse_args(argv)

    if args.ignore_warn:
        ciur.CONF["IGNORE_WARNING"] = args.ignore_warn

    return pretty_parse_from_resources(args.rule, args.parse)


def main():
    print(parse_cli(*sys.argv[1:]))
