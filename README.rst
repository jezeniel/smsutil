smsutil - encode, decode and split SMS
======================================

Simple set of utility functions for encoding, decoding and splitting
sms messages. Shift tables is currently not supported.


Features
--------

- Codecs for encoding and decoding `GSM 03.38 <https://en.wikipedia.org/wiki/GSM_03.38>`_
- Message splitting for both ``UCS2/UTF-16`` and ``GSM 03.38``


Installation
------------

To install ``smsutil``:

.. code-block:: bash

  $ pip install smsutil


Basic Usage
-----------

Example for encoding and decoding:

.. code-block:: python

  import smsutil

  smsutil.is_valid_gsm('nobita and doraemon')  # True
  smsutil.is_valid_gsm('🍔')  # False

  gsm = smsutil.encode('the quick brown fox jumps over the lazy dog {@}')
  # b'the quick brown fox jumps over the lazy dog \x1b(\x00\x1b)'
  smsutil.decode(gsm)  # encoding='gsm0338'
  # 'the quick brown fox jumps over the lazy dog {@}'

  utf16 = smsutil.encode('最高でした 🍔')
  # b'g\x00\x9a\xd80g0W0_\x00 \xd8<\xdfT'
  smsutil.decode(utf16, encoding='utf_16_be')  # should specify encoding
  # '最高でした 🍔'

  sms = smsutil.split('[the quick brown fox]')
  len(sms.parts)  # 1
  sms.encoding  # 'gsm0338'
  sms.parts[0].content  # 'the quick brown fox.'
  sms.parts[0].length  # 21
  sms.parts[0].bytes  # 23

  sms = smsutil.split('最高でした 🍔')
  len(sms.parts) # 1
  sms.encoding  # 'utf_16_be'
  sms.parts[0].content  # '最高でした 🍔'
  sms.parts[0].length  # 7
  sms.parts[0].bytes  # 16

smsutil is just using python's builtin codecs for UCS2/UTF-16.


Contributing
------------

1. Fork repository.
2. Create a pull request.
3. ✨🍰✨
