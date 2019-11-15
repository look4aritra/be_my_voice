# -*- coding: utf-8 -*-
# %%
import re
import xml.etree.ElementTree as et
from contextlib import suppress

tag_re = re.compile(r'<[^>]+>')


# %%
def list2string(data):
    out = ''
    with suppress(Exception):
        out = ' '.join(map(str, data))
    # print(out)
    return out


# %%
def print_dataframe(data):
    for row in data.itertuples(index=False):
        print(row)


# %%
def sanitize(text):
    sanitized = text
    # remove tags if standard html document
    with suppress(Exception):
        sanitized = ''.join(et.fromstring(text).itertext())
    # remove any lingering tags
    with suppress(Exception):
        sanitized = tag_re.sub('', text)
    with suppress(Exception):
        sanitized = sanitized.replace('\\', ' ').replace('/', ' ')
    # remove eol and eol whitespace, including multiple consecutive ones
    sanitized = ' '.join(sanitized.rstrip().split())
    # print(sanitized)
    return sanitized


# %%
def remove_stopwords(sen, stop_words):
    sen_new = ' '.join([i for i in sen if i not in stop_words])
    # print(sen_new)
    return sen_new

# %%
# print(list2string(['hey', 'there']))

# print(sanitize(''))
# print(sanitize('hello'))
# print(sanitize('<cust>hello</cust>'))
# print(sanitize('<html>hello</html> all'))
# print(sanitize('<html>hello</html> \r\r   \nall'))
