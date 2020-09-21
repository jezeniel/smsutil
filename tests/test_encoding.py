# -*- coding:  utf-8 -*-
from __future__ import unicode_literals

import unittest

from smsutil.codecs import GSM_CHARSET, is_valid_gsm, text_to_gsm, count_non_gsm_characters


class TestGSMValidator:
    def test_charset(self):
        assert is_valid_gsm(GSM_CHARSET)

    def test_mixed(self):
        assert not is_valid_gsm('the quick brown 🍔')

    def test_invalid_characters(self):
        assert not is_valid_gsm('the quick brown こんにちは')

    def test_text_to_gsm(self):
        test_string = '|最Som€高でした 	Text	🍔!'
        assert text_to_gsm(test_string) == "|Som€ Text!"
        assert text_to_gsm(test_string, True) == "Som Text!"

    def count_non_gsm_characters(self):
        test_string = '|最Som€高でした 	Text	🍔!'
        assert count_non_gsm_characters(test_string) == 7
        assert count_non_gsm_characters(test_string, True) == 5


class TestCoding(unittest.TestCase):
    def test_roundtrip(self):
        gsm7_charset_without_control_chars = (
            '@£$¥èéùìòÇ\nØø\rÅåΔ_ΦΓΛΩΠΨΣΘΞÆæßÉ !"#¤%&\'()*+,-./0123456789:;<=>?¡'
            'ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÑÜ§¿abcdefghijklmnopqrstuvwxyzäöñüà'
            '^{}\\[~]|€'
        )
        encoded = gsm7_charset_without_control_chars.encode('gsm7')
        decoded = encoded.decode('gsm7')
        self.assertEqual(decoded, gsm7_charset_without_control_chars)
