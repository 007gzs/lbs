# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import unittest

from lbs.core.utils import ObjectDict, LbsMd5Signer


class UtilityTestCase(unittest.TestCase):

    def test_object_dict(self):
        obj = ObjectDict()
        self.assertTrue(obj.xxx is None)
        obj.xxx = 1
        self.assertEqual(1, obj.xxx)

    def test_md5_signer(self):

        signer = LbsMd5Signer(end="123")
        signer.add_data('789')
        signer.add_data('456')
        signer.add_data('123')
        signature = signer.signature

        self.assertEqual('df96220fa161767c5cbb95567855c86b', signature)
