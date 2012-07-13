#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright ${year}
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
'''
:mod:`tier_3_mn_storage_create`
===============================

:Created: 2011-04-22
:Author: DataONE (Dahl)
:Dependencies:
  - python 2.6
'''

# Std.
import datetime
import os
import random
import sys
import time
import uuid
import xml.sax.saxutils
import StringIO

# D1.
import d1_common.const
import d1_common.types.exceptions
import d1_common.types.generated.dataoneTypes as dataoneTypes

import d1_client.mnclient

import d1_instance_generator
import d1_instance_generator.random_data
import d1_instance_generator.systemmetadata
import d1_instance_generator.accesspolicy

# App.
_here = lambda *x: os.path.join(os.path.abspath(os.path.dirname(__file__)), *x)
sys.path.append(_here('../../../shared/'))
import settings
import subject_dn

# Config

# The number of bytes in each science object.
n_sci_obj_bytes = 1024

# The number of subjects to allow access to each created test object.
n_allow = 10


class Transaction(object):
  def __init__(self):
    self.custom_timers = {}

  def run(self):
    start_timer = time.time()
    self.create_test_file_on_member_node()
    latency = time.time() - start_timer
    self.custom_timers['create'] = latency

  def create_test_file_on_member_node(self):
    sci_obj = self.create_science_object()
    subjects = self.create_list_of_random_subjects(n_allow)
    access_policy = self.create_access_policy(subjects)
    sys_meta = self.create_system_metadata(sci_obj, access_policy)
    client = self.create_client()
    try:
      res = client.create(sys_meta.identifier.value(), sci_obj, sys_meta)
    except Exception as e:
      with open('/tmp/stress_test_error.html', 'w') as f:
        f.write(str(e))
      raise

  def create_science_object(self):
    return d1_instance_generator.random_data.random_bytes_flo(n_sci_obj_bytes)

  def create_system_metadata(self, sci_obj, access_policy):
    return d1_instance_generator.systemmetadata.generate_from_flo(
      sci_obj, {'accessPolicy': access_policy}
    )

  def create_access_policy(self, subjects):
    ap = dataoneTypes.AccessPolicy()
    ar = dataoneTypes.AccessRule()
    for subject in subjects:
      ar.subject.append(
        subject_dn.get_dataone_compliant_dn_serialization_by_subject(subject)
      )
      ar.permission = ['changePermission']
    ap.allow.append(ar)
    return ap

  def create_client(self):
    cert_path = os.path.join(
      settings.CLIENT_CERT_DIR, settings.SUBJECT_WITH_CREATE_PERMISSIONS
    )
    key_path = settings.CLIENT_CERT_PRIVATE_KEY_PATH
    return d1_client.mnclient.MemberNodeClient(
      base_url=settings.BASEURL,
      cert_path=cert_path,
      key_path=key_path
    )

  def get_subject_list(self):
    with open(settings.SUBJECTS_PATH, 'r') as f:
      return filter(None, f.read().split('\n'))

  def create_list_of_random_subjects(self, n_subjects):
    return random.sample(self.get_subject_list(), n_subjects)


if __name__ == '__main__':
  t = Transaction()
  t.run()
  #import cProfile
  #cProfile.run('t.run()', 'profile')
