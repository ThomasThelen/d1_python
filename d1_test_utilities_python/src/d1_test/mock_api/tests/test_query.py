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

import unittest

# D1
import d1_client.mnclient_2_0
import d1_common.const
import d1_common.date_time
import d1_common.types.exceptions
import d1_common.util

# 3rd party
import requests
import responses

# App
import d1_test.mock_api.query as mock_query
import d1_test.mock_api.tests.settings as settings


class TestMockQuery(unittest.TestCase):
  @classmethod
  def setUpClass(cls):
    d1_common.util.log_setup(is_debug=True)

  def setUp(self):
    self.client = d1_client.mnclient_2_0.MemberNodeClient_2_0(
      base_url=settings.MN_RESPONSES_BASE_URL
    )

  @responses.activate
  def test_0010(self):
    """mock_api.query() returns a JSON doc with expected structure"""
    mock_query.add_callback(settings.MN_RESPONSES_BASE_URL)
    response = self.client.query('query_engine', 'query_string')
    self.assertIsInstance(response, requests.Response)
    self.assertEqual(response.headers['Content-Type'], 'application/json')
    response_dict = response.json()
    self.assertIn(u'User-Agent', response_dict['header_dict'])
    del response_dict['header_dict']['User-Agent']
    expected_dict = {
      u'body_base64': u'PG5vIGJvZHk+',
      u'query_dict': {},
      u'header_dict': {
        u'Connection': u'keep-alive',
        u'Charset': u'utf-8',
        u'Accept-Encoding': u'gzip, deflate',
        u'Accept': u'*/*',
      }
    }
    self.assertDictEqual(response_dict, expected_dict)

  @responses.activate
  def test_0011(self):
    """mock_api.query(): Passing a trigger header triggers a DataONEException"""
    mock_query.add_callback(settings.MN_RESPONSES_BASE_URL)
    self.assertRaises(
      d1_common.types.exceptions.NotAuthorized, self.client.query,
      'query_engine', 'query_string', vendorSpecific={'trigger': '401'}
    )
