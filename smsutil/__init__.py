from __future__ import absolute_import, unicode_literals
from  collections import namedtuple
from .codecs import is_valid_gsm0338, GSM_BASIC_CHARSET, GSM_EXT_CHARSET


Part = namedtuple('Part', ['content', 'bytes', 'length'])


def encode(text):
    if is_valid_gsm0338(text):
        encoding = 'gsm0338'
    else:
        encoding = 'utf_16_be'
    return text.encode(encoding)


def decode(bytestring, encoding='gsm0338'):
    return bytestring.decode(encoding)


def gsm_split(text):
    SINGLE_PART_BYTES = 160
    MULTI_PART_BYTES = 153

    parts = []
    total_bytes = 0
    total_length = len(text)

    message = ''
    bytes = 0
    for char in text:
        message += char
        bytes += 1
        extended = False
        if char in GSM_EXT_CHARSET:
            bytes += 1
            extended = True
        if bytes > MULTI_PART_BYTES:
            # remove added bytes and don't include current char
            bytes -= 1
            if extended:
                bytes -= 1
            parts.append(Part(message[:-1], bytes, len(message) - 1))
            message = char
            total_bytes += bytes
            bytes = 1
            if extended:
                bytes += 1
    if message:
        parts.append(Part(message, bytes, len(message)))
        total_bytes += bytes
    if total_bytes <= SINGLE_PART_BYTES:
        parts = [Part(text, total_bytes, total_length)]
    return parts


def unicode_split():
    pass


def split(text):
    bstring = encode(text)
