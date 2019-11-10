# -*- coding: utf-8 -*-

import re
import xml.etree.ElementTree as et

from contextlib import suppress


tag_re = re.compile(r'<[^>]+>')


def list2string(data):
    out = ''
    with suppress(Exception):
        out = ' '.join(map(str, data))
    # print(out)
    return out


def print_dataframe(data):
    for row in data.itertuples(index=False):
        print(row)


def sanitize(text):
    sanitized = text
    # remove tags if standard html document
    with suppress(Exception):
        sanitized = ''.join(et.fromstring(text).itertext())
    # remove any lingering tags
    with suppress(Exception):
        sanitized = tag_re.sub('', text)
    # remove eol and eol whitespace, including multiple consecutive ones
    sanitized = " ".join(sanitized.rstrip().split())
    print(sanitized)
    return sanitized
