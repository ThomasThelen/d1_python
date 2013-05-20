#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2012 DataONE
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
"""
:mod:`setup`
============

:Synopsis: Create egg.
:Author: DataONE (Dahl)
"""

from setuptools import setup, find_packages
import d1_workspace

setup(
  name='dataone.workspace_client',
  version=d1_workspace.__version__,
  description='A DataONE Workspace client library for Python',
  author='DataONE Project',
  author_email='developers@dataone.org',
  url='http://dataone.org',
  license='Apache License, Version 2.0',
  packages=find_packages(),

  # Accept all data files and directories matched by MANIFEST.in or found in
  # source control.
  include_package_data=True,

  # Specify additional patterns to match files and directories that may or may
  # not be matched by MANIFEST.in or found in source control.
  package_data={
    #'': ['*.txt', '*.rst', '*.csv'],
  },

  # Specify patterns for data files and directories that should not be included
  # when a package is installed, even if they would otherwise have been included
  # due to the use of the preceding options.
  exclude_package_data={
    '': ['*.log', '*.txt'],
  },

  # Dependencies that are available through PYPI / easy_install.
  install_requires=[
    #'dataone.common >= 1.0.0',
    #'rdflib < 3a',
    #'google.foresite-toolkit == 1.2',
  ],
)
