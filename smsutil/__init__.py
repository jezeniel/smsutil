# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from .codecs import is_valid_gsm, GSM_EXT_CHARSET

GSM_SINGLE_PART_BYTES = 160
GSM_MULTI_PART_BYTES = 153

UNICODE_SINGLE_PART_BYTES = 140
UNICODE_MULTI_PART_BYTES = 134


class SplitResult:
    def __init__(self, parts=[], total_bytes=0, total_length=0, encoding=None):
        self.encoding = encoding
        self.parts = parts
        self.total_bytes = total_bytes
        self.total_length = total_length

    def __repr__(self):
        return '<SplitResult {!r}>'.format(self.parts)


class Part:
    def __init__(self, content, bytes=0, length=0):
        self.content = content
        self.bytes = bytes
        self.length = length

    def __repr__(self):
        return '<Part "{!r}">'.format(self.content)


def encode(text):
    '''Encodes text.
    Checks if text is a valid `gsm0338` the uses `utf_16_be` if not.
    '''
    if is_valid_gsm(text):
        encoding = 'gsm0338'
    else:
        encoding = 'utf_16_be'
    return text.encode(encoding)


def decode(bytestring, encoding='gsm0338'):
    return bytestring.decode(encoding)


def gsm_split(text, multi_part_bytes=GSM_MULTI_PART_BYTES,
              single_part_bytes=GSM_SINGLE_PART_BYTES):
    ''' Split gsm 03.38 text. '''
    if not is_valid_gsm(text):
        raise ValueError('text is not a valid gsm0338 value.')

    BYTES_PER_CHAR = 1

    parts = []
    total_bytes = 0

    message = ''
    bytes = 0
    for char in text:
        char_byte = BYTES_PER_CHAR
        bytes += BYTES_PER_CHAR
        message += char
        if char in GSM_EXT_CHARSET:
            bytes += BYTES_PER_CHAR
            char_byte += BYTES_PER_CHAR
        if bytes > multi_part_bytes:
            # remove added bytes and don't include current char
            bytes -= char_byte
            parts.append(Part(message[:-1], bytes, len(message) - 1))
            total_bytes += bytes

            # use current char to the next part
            message = char
            bytes = char_byte
    if message:
        parts.append(Part(message, bytes, len(message)))
        total_bytes += bytes
    if total_bytes <= single_part_bytes:
        parts = [Part(text, total_bytes, len(text))]

    result = SplitResult(
        encoding='gsm0338', parts=parts, total_bytes=total_bytes,
        total_length=len(text)
    )
    return result


def unicode_split(text, multi_part_bytes=UNICODE_MULTI_PART_BYTES,
                  single_part_bytes=UNICODE_SINGLE_PART_BYTES):
    ''' Split ucs2/utf-16 text. '''
    BYTES_PER_CHAR = 2

    parts = []
    total_bytes = 0

    message = ''
    bytes = 0
    for char in text:
        char_byte = BYTES_PER_CHAR
        bytes += BYTES_PER_CHAR
        message += char
        # check if surrogate pair
        if ord(char) >= 0x10000 and ord(char) <= 0x10ffff:
            bytes += BYTES_PER_CHAR
            char_byte += BYTES_PER_CHAR
        if bytes > multi_part_bytes:
            # remove added bytes and don't include current char
            bytes -= char_byte
            parts.append(Part(message[:-1], bytes, len(message) - 1))
            total_bytes += bytes

            # use current `char` for the next part
            message = char
            bytes = char_byte
    if message:
        parts.append(Part(message, bytes, len(message)))
        total_bytes += bytes
    if total_bytes <= single_part_bytes:
        parts = [Part(text, total_bytes, len(text))]

    result = SplitResult(
        encoding='utf_16_be', parts=parts,
        total_bytes=total_bytes, total_length=len(text)
    )
    return result


def split(text, *args, **kwargs):
    if is_valid_gsm(text):
        return gsm_split(text, *args, **kwargs)
    else:
        return unicode_split(text, *args, **kwargs)
