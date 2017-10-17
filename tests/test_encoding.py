# -*- coding:  utf-8 -*-
from smsutil.codecs import GSM_CHARSET, is_valid_gsm


class TestGSMValidator:
    def test_charset(self):
        assert is_valid_gsm(GSM_CHARSET)

    def test_mixed(self):
        assert not is_valid_gsm('the quick brown 🍔')

    def test_invalid_characters(self):
        assert not is_valid_gsm('the quick brown こんにちは')
