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

import xml.sax

import pyxb

import d1_test.d1_test_case


class TestLogRecords(d1_test.d1_test_case.D1TestCase):
  parameterize_dict = {
    'test_0010': [
      dict(filename='log_gmn_valid.xml', shouldfail=False),
      dict(filename='log_knb_valid.xml', shouldfail=False),
      dict(filename='log_invalid_1.xml', shouldfail=True),
      dict(filename='log_invalid_2.xml', shouldfail=True),
      dict(filename='log_invalid_3.xml', shouldfail=True),
    ],
  }

  def test_0010(self, filename, shouldfail):
    """Deserialize various Log XML docs"""
    try:
      self.read_xml_file_to_pyxb(filename)
    except (pyxb.PyXBException, xml.sax.SAXParseException):
      if not shouldfail:
        raise
