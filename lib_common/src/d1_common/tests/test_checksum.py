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
import json
import xml.sax

import pytest
import pyxb

import d1_common.checksum
import d1_common.const
import d1_common.types.dataoneTypes as dataoneTypes

import d1_test.d1_test_case

# App


class TestChecksum(d1_test.d1_test_case.D1TestCase):
  parameterize_dict = {
    'test_0010': [
      dict(filename='checksum_gmn_valid.xml', shouldfail=False),
      dict(filename='checksum_invalid_1.xml', shouldfail=True),
      dict(filename='checksum_invalid_2.xml', shouldfail=True),
    ],
  }

  def test_0010(self, filename, shouldfail):
    """Deserialize: XML -> Checksum"""
    exp_json = self.read_sample_file(filename)
    exp_dict = json.loads(exp_json)
    try:
      checksum_pyxb = dataoneTypes.CreateFromDocument(exp_dict['xml'])
    except (pyxb.PyXBException, xml.sax.SAXParseException):
      if not shouldfail:
        raise
    else:
      assert checksum_pyxb.algorithm == exp_dict['algorithm']
      assert checksum_pyxb.value() == exp_dict['checksum']

  def test_0040(self):
    """Serialization: Checksum -> XML -> Checksum"""
    checksum_obj_in = dataoneTypes.checksum('1' * 32)
    checksum_obj_in.algorithm = 'MD5'
    checksum_xml = checksum_obj_in.toxml('utf-8')
    checksum_obj_out = dataoneTypes.CreateFromDocument(checksum_xml)
    assert checksum_obj_in.value() == checksum_obj_out.value()
    assert checksum_obj_in.algorithm == checksum_obj_out.algorithm

  def test_0050(self):
    """checksums_are_equal(): Same checksum, same algorithm"""
    c1 = dataoneTypes.Checksum('BAADF00D')
    c1.algorithm = 'SHA-1'
    c2 = dataoneTypes.Checksum('BAADF00D')
    c2.algorithm = 'SHA-1'
    assert d1_common.checksum.are_checksums_equal(c1, c2)

  def test_0060(self):
    """checksums_are_equal(): Same checksum, different algorithm"""
    c1 = dataoneTypes.Checksum('BAADF00D')
    c1.algorithm = 'SHA-1'
    c2 = dataoneTypes.Checksum('BAADF00D')
    c2.algorithm = 'MD5'
    with pytest.raises(ValueError):
      d1_common.checksum.are_checksums_equal(c1, c2)

  def test_0070(self):
    """checksums_are_equal(): Different checksum, same algorithm"""
    c1 = dataoneTypes.Checksum('BAADF00DX')
    c1.algorithm = 'MD5'
    c2 = dataoneTypes.Checksum('BAADF00D')
    c2.algorithm = 'MD5'
    assert not d1_common.checksum.are_checksums_equal(c1, c2)

  def test_0080(self):
    """checksums_are_equal(): Case insensitive checksum comparison"""
    c1 = dataoneTypes.Checksum('baadf00d')
    c1.algorithm = 'MD5'
    c2 = dataoneTypes.Checksum('BAADF00D')
    c2.algorithm = 'MD5'
    assert d1_common.checksum.are_checksums_equal(c1, c2)

  def test_0090(self):
    """get_checksum_calculator_by_dataone_designator() returns a checksum calculator"""
    calculator = d1_common.checksum.get_checksum_calculator_by_dataone_designator(
      'SHA-1'
    )
    calculator.update('test')
    assert calculator.hexdigest()

  def test_0100(self):
    """get_checksum_calculator_by_dataone_designator() raises on invalid algorithm"""
    with pytest.raises(Exception):
      d1_common.checksum.get_checksum_calculator_by_dataone_designator(
        'SHA-224-bogus'
      )
