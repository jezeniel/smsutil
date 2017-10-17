from __future__ import absolute_import, unicode_literals
from collections import namedtuple
from .codecs import is_valid_gsm0338, GSM_EXT_CHARSET


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

    message = ''
    bytes = 0
    for char in text:
        char_byte = 1
        message += char
        bytes += 1
        if char in GSM_EXT_CHARSET:
            bytes += 1
            char_byte += 1
        if bytes > MULTI_PART_BYTES:
            # remove added bytes and don't include current char
            bytes -= char_byte
            parts.append(Part(message[:-1], bytes, len(message) - 1))
            total_bytes += bytes

            # move current char to the next part
            message = char
            bytes = char_byte
    if message:
        parts.append(Part(message, bytes, len(message)))
        total_bytes += bytes
    if total_bytes <= SINGLE_PART_BYTES:
        parts = [Part(text, total_bytes, len(text))]
    return parts


def unicode_split():
    pass
