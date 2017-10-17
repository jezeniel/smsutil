# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytest

import smsutil


class TestEncode:
    def test_encode_gsm(self):
        assert smsutil.encode('{@}') == b'\x1b\x28\x00\x1b\x29'

    def test_encode_ucs2(self):
        assert smsutil.encode('ちは') == b'\x30\x61\x30\x6f'


class TestGsmSplit:
    def test_unicode_value(self):
        with pytest.raises(ValueError):
            smsutil.gsm_split('ちは')

    def test_one_part(self):
        text = '1' * 160
        parts = smsutil.gsm_split(text)
        assert len(parts) == 1
        assert len(parts[0].content) == parts[0].length
        assert parts[0].length == 160
        assert parts[0].bytes == 160
        assert parts[0].content == text

    def test_two_part(self):
        text = '1' * 160 + '2' * 10
        parts = smsutil.gsm_split(text)
        assert len(parts) == 2
        assert len(parts[0].content) == parts[0].length
        assert parts[0].content == text[0:153]
        assert parts[0].bytes == 153

        assert len(parts[1].content) == parts[1].length
        assert parts[1].content == text[153:]
        assert parts[1].bytes == 17

    def test_basic_and_ext(self):
        text = '1' * 145 + '{' * 15
        parts = smsutil.gsm_split(text)
        assert len(parts) == 2
        assert len(parts[0].content) == parts[0].length
        assert parts[0].length == 149
        assert parts[0].content == text[0:149]
        assert parts[0].bytes == 153

        assert len(parts[1].content) == parts[1].length
        assert parts[1].length == 11
        assert parts[1].content == text[149:]
        assert parts[1].bytes == 22

    def test_basic_and_ext2(self):
        text = (
            '111111111111111111111111111111111111111111111111'
            '111111111111111111111111111111111111111111111111'
            '111111111111111111111111111111111111111111111111'
            '11111111{111111111111'
        )
        parts = smsutil.gsm_split(text)
        assert len(parts) == 2
        assert len(parts[0].content) == parts[0].length
        assert parts[0].length == 152
        assert parts[0].content == text[0:152]
        assert parts[0].bytes == 152

        assert len(parts[1].content) == parts[1].length
        assert parts[1].length == 13
        assert parts[1].content == text[152:]
        assert parts[1].bytes == 14


class TestUnicodeSplit:
    def test_non_pair_detection(self):
        parts = smsutil.unicode_split('ち')
        assert len(parts) == 1
        assert parts[0].bytes == 2

    def test_pair_detection(self):
        parts = smsutil.unicode_split('🍔')  # hamburger emoji
        assert len(parts) == 1
        assert parts[0].bytes == 4

    def test_pair_detection_multipart(self):
        parts = smsutil.unicode_split('🍔' * 80)  # hamburger emoji
        assert len(parts) == 3
        assert parts[0].bytes == 132
        assert parts[1].bytes == 132
        assert parts[2].bytes == 56

        assert parts[0].length == 33
        assert parts[1].length == 33
        assert parts[2].length == 14

    def test_one_part(self):
        text = 'ち' * 70
        parts = smsutil.unicode_split(text)
        assert len(parts) == 1
        assert len(parts[0].content) == parts[0].length
        assert parts[0].length == 70
        assert parts[0].bytes == 140
        assert parts[0].content == text

    def test_two_part(self):
        text = 'ち' * 70 + 'は' * 10
        parts = smsutil.unicode_split(text)
        assert len(parts) == 2
        assert len(parts[0].content) == parts[0].length
        assert parts[0].length == 67
        assert parts[0].content == text[0:67]
        assert parts[0].bytes == 134

        assert len(parts[1].content) == parts[1].length
        assert parts[1].length == 13
        assert parts[1].content == text[67:]
        assert parts[1].bytes == 26

    def test_basic_and_ext2(self):
        text = (
            'ちちちちちちちちちちちちちちちちちちちちちちちちちち'
            'ちちちちちちちちちちちちちちちちちちちちちちちちちち'
            'ちちちちちちちちちちちちちちはちちちち'
        )
        parts = smsutil.unicode_split(text)
        assert len(parts) == 2
        assert len(parts[0].content) == parts[0].length
        assert parts[0].length == 67
        assert parts[0].content == text[0:67]
        assert parts[0].bytes == 134

        assert len(parts[1].content) == parts[1].length
        assert parts[1].length == 4
        assert parts[1].content == text[67:]
        assert parts[1].bytes == 8
