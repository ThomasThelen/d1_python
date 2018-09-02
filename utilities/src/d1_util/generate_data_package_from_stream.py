#!/usr/bin/env python

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2017 DataONE
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
"""Generate a Data Package (Resource Map) from a stream of PIDs

This is an example on how to use the DataONE Client and Common libraries for
Python.
"""

import logging

from resource_map import ResourceMap


def createSimpleResourceMap(ore_pid, sci_meta_pid, data_pids):
  """Create a simple resource map with one metadata document and n data
  objects."""
  ore = ResourceMap()
  ore.oreInitialize(ore_pid)
  ore.addMetadataDocument(sci_meta_pid)
  ore.addDataDocuments(data_pids, sci_meta_pid)
  return ore


def pids2ore(in_stream, fmt='xml', base_url='https://cn.dataone.org/cn'):
  """read pids from in_stream and generate a resource map.

  first pid is the ore_pid second is the sci meta pid remainder are data
  pids
  """
  pids = []
  for line in in_stream:
    pid = line.strip()
    if len(pid) > 0:
      if not pid.startswith("# "):
        pids.append(pid)
  if (len(pids)) < 2:
    raise ValueError("Insufficient identifiers provided.")

  logging.info("Read %d identifiers", len(pids))

  ore = ResourceMap(base_url=base_url)

  logging.info("ORE PID = %s", pids[0])
  ore.oreInitialize(pids[0])

  logging.info("Metadata PID = %s", pids[1])
  ore.addMetadataDocument(pids[1])

  ore.addDataDocuments(pids[2:], pids[1])
  return ore.serialize(doc_format=fmt)