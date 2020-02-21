# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import
from builtins import chr
import codecs
import re

from builtins import bytes


GSM_BASIC_CHARSET = (
    u'@£$¥èéùìòÇ\nØø\rÅåΔ_ΦΓΛΩΠΨΣΘΞ\x1bÆæßÉ !"#¤%&\'()*+,-./0123456789:;<=>?¡'
    u'ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÑÜ§¿abcdefghijklmnopqrstuvwxyzäöñüà')

GSM_EXT_CHARSET = u'\f^{}\\[~]|€'

GSM_CHARSET = GSM_BASIC_CHARSET + GSM_EXT_CHARSET

basic_pairs = dict(zip(
    [i for i in range(len(GSM_BASIC_CHARSET))],
    [ord(c) for c in GSM_BASIC_CHARSET],
))

ext_pairs = dict(zip(
    [bytes([ord('\x1b'), ord(c)])
     for c in '\x0a\x14\x28\x29\x2f\x3c\x3d\x3e\x40\x65'],
    [ord(c) for c in GSM_EXT_CHARSET]
))

decoding_map = basic_pairs
decoding_map.update(ext_pairs)

encoding_map = codecs.make_encoding_map(decoding_map)


def decode_gsm0338(text, decoding_map):
    ESCAPE = ord('\x1b')
    SPACE = ord(' ')
    decoded = u''
    skip = None
    for index, char in enumerate(bytes(text)):
        next = index + 1
        if skip == index:
            continue
        if char != ESCAPE:
            d = decoding_map.get(char)
        elif char == ESCAPE and next < len(text):
            ext_char = bytes([ESCAPE, text[next]])
            d = decoding_map.get(ext_char, SPACE)
            if d != SPACE:
                skip = next
        else:
            d = SPACE
        decoded += chr(d)
    return decoded, len(decoded)


class GSM0338Codec(codecs.Codec):
    def encode(self, input, errors='strict'):
        return codecs.charmap_encode(input, errors, encoding_map)

    def decode(self, input, errors='strict'):
        return decode_gsm0338(input, decoding_map)


class GSM0338IncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input, final=False):
        return codecs.charmap_encode(input, self.errors, encoding_map)[0]


class GSM0338IncrementalDecoder(codecs.IncrementalDecoder):
    def decode(self, input, final=False):
        return decode_gsm0338(input, decoding_map)[0]


class GSM0338StreamReader(GSM0338Codec, codecs.StreamReader):
    pass


class GSM0338StreamWriter(GSM0338Codec, codecs.StreamWriter):
    pass


def search_gsm0338(encoding):
    if encoding in ('gsm0338', 'gsm7'):
        return codecs.CodecInfo(
            name='gsm0338',
            encode=GSM0338Codec().encode,
            decode=GSM0338Codec().decode,
            incrementalencoder=GSM0338IncrementalEncoder,
            incrementaldecoder=GSM0338IncrementalDecoder,
            streamwriter=GSM0338StreamWriter,
            streamreader=GSM0338StreamReader
        )
    return None


def is_valid_gsm(text):
    ''' Validate if `text` is a valid gsm 03.338.  '''
    r = u'^[' + re.escape(GSM_CHARSET) + ']+$'
    return re.match(r, text, re.UNICODE) is not None


codecs.register(search_gsm0338)
