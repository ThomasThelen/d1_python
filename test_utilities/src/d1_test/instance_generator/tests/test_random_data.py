#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2016 DataONE
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import random
import unittest

import d1_test.d1_test_case
import d1_test.instance_generator.random_data as random_data

#===============================================================================


class TestRandomData(d1_test.d1_test_case.D1TestCase):
  def setUp(self):
    pass

  def _assert_unique(self, unique_list):
    count = {}
    for item in unique_list:
      try:
        count[item] += 1
      except LookupError:
        count[item] = 1
      assert len(item) > 0
    for name, count in count.items():
      assert count == 1

  def test_0010(self):
    """random_bytes()"""
    s = random_data.random_bytes(1000)
    assert len(s) == 1000

  def test_0020(self):
    """random_unicode_name()"""
    name = random_data.random_unicode_name()
    assert len(name) > 0
    assert isinstance(name, unicode)

  def test_0030(self):
    """random_unicode_name_list()"""
    names = random_data.random_unicode_name_list(10)
    assert len(names) == 10
    for name in names:
      assert len(names) > 0
      assert isinstance(name, unicode)

  def test_0040(self):
    """random_unicode_name_unique_list()"""
    for i in range(10):
      names = random_data.random_unicode_name_unique_list(30)
      assert len(names) == 30
      assert isinstance(names[0], unicode)
      self._assert_unique(names)

  def test_0050(self):
    """random_word()"""
    word = random_data.random_word()
    assert len(word) > 0
    assert isinstance(word, unicode)

  def test_0060(self):
    """random_3_words()"""
    words = random_data.random_3_words()
    assert len(words) > 0
    assert isinstance(words, unicode)

  def test_0070(self):
    """random_word_list()"""
    words = random_data.random_word_list(10)
    assert len(words) == 10
    for word in words:
      assert len(words) > 0
      assert isinstance(word, unicode)

  def test_0080(self):
    """random_word_unique_list()"""
    for i in range(10):
      names = random_data.random_word_unique_list(30)
      assert len(names) == 30
      assert isinstance(names[0], unicode)
      self._assert_unique(names)

  def test_0090(self):
    """random_unicode_string()"""
    for i in range(10):
      min_len = random.randint(0, 100)
      max_len = random.randint(min_len, 100)
      s = random_data.random_unicode_string_no_whitespace(min_len, max_len)
      assert len(s) >= min_len
      assert len(s) <= max_len

  def test_0100(self):
    """random_email()"""
    for i in range(10):
      s = random_data.random_email()
      assert s

  def test_0110(self):
    """random_bool()"""
    for i in range(10):
      b = random_data.random_bool()
      assert isinstance(b, bool)


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO)
  unittest.main()
