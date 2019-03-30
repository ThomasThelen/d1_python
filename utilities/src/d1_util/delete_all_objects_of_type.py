#!/usr/bin/env python

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
"""Delete all Science Objects of specific type from Member Node.

This is an example on how to use the DataONE Client and Common libraries for Python. It
shows how to:

- Retrieve a list of all objects with specific FormatID on a Member Node
- Delete all objects with a specific FormatID from a Member Node

Notes:

- Do NOT use this script to delete undesired objects from a production Member Node!

- The objects are deleted with the MNStorage.delete() API method. The API method is
  intended to be called only by CNs under specific circumstances. In a stand-alone or
  non-production environment, the API can be used for removing objects from a Member
  Node.

- MNStorage.delete() is only available to subjects which have delete permission on the
  node.

- To delete all the objects on the node, remove the formatId and replicaStatus
  parameters in the listObjects() call below.

- The Member Node object list is retrieved in small sections, called pages. Because
  removing objects may, depending on the implementation of listObjects(), cause the
  contents in each page to shift, the entire list of objects to delete is created first
  and then the deletions are performed in a separate step. This could require a lot of
  memory if running on a server with a large number of objects. In that case, an
  alternative implementation is to delete the objects as they are discovered and repeat
  the process until no more objects to delete are found.

- The listObjects() Member Node API method may not be efficiently implemented by all
  Member Nodes as it is intended primarily for use by Coordinating Nodes.

Operation:

- Configure the script in the Config section below

"""
import argparse
import logging
import sys

import d1_common.const
import d1_common.env
import d1_common.types.exceptions

# Config

# The Member Node from which objects are deleted.
MEMBER_NODE_BASE_URL = 'http://127.0.0.1:8000'

# Delete objects of this type. A complete list of valid formatIds can be
# found at https://cn.dataone.org/cn/v1/formats
LIST_OBJECTS_FORMAT_ID = 'eml://ecoinformatics.org/eml-2.0.0'

# The number of objects to list each time listObjects() is called.
LIST_OBJECTS_PAGE_SIZE = 100

# Paths to the certificate and key to use when deleting the objects. If the
# certificate has the key embedded, the _KEY setting should be set to None. The
# Member Node must trust the certificate and allow access to
# MNStorage.listObjects() and MNStorage.delete() for the certificate subject. If
# the target Member Node is a DataONE Generic Member Node (GMN) instance, see
# the "Using GMN" section in the documentation for GMN for information on how to
# create and use certificates. The information there may be relevant for other
# types of Member Nodes as well.
CERTIFICATE = 'client.crt'
CERTIFICATE_KEY = 'client.key'


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--debug', action='store_true', help='Debug level logging')
    parser.add_argument(
        '--env',
        type=str,
        default='prod',
        help='Environment, one of {}'.format(', '.join(d1_common.env.D1_ENV_DICT)),
    )
    parser.add_argument(
        '--cert-pub',
        dest='cert_pem_path',
        action='store',
        help='Path to PEM formatted public key of certificate',
    )
    parser.add_argument(
        '--cert-key',
        dest='cert_key_path',
        action='store',
        help='Path to PEM formatted private key of certificate',
    )
    parser.add_argument(
        '--timeout',
        action='store',
        default=d1_common.const.DEFAULT_HTTP_TIMEOUT,
        help='Amount of time to wait for calls to complete (seconds)',
    )

    # Setting the default logger to level "DEBUG" causes the script to become
    # very verbose.
    logging.basicConfig()
    logging.getLogger('').setLevel(logging.DEBUG)

    member_node_object_deleter = MemberNodeObjectDeleter(MEMBER_NODE_BASE_URL)
    member_node_object_deleter.delete_objects_from_member_node()


# ==============================================================================


class MemberNodeObjectDeleter(object):
    def __init__(self, base_url):
        self._base_url = base_url
        self._mn_client = d1_client.mnclient_2_0.MemberNodeClient_2_0(
            self._base_url, cert_pem_path=CERTIFICATE, cert_key_path=CERTIFICATE_KEY
        )

    def delete_objects_from_member_node(self):
        logging.info(
            'Searching for objects to delete on Member Node: {}'.format(self._base_url)
        )
        pids_delete = self._find_objects_to_delete()
        logging.info('Found {} objects to delete'.format(len(pids_delete)))
        if not len(pids_delete):
            return
        self._delete_objects(pids_delete)
        # Check for success.
        pids_remaining = self._find_objects_to_delete()
        if len(pids_remaining):
            logging.error(
                'Deletion failed on {} of {} objects'.format(
                    len(pids_remaining), len(pids_delete)
                )
            )
        else:
            logging.info('Successfully deleted {} objects'.format(len(pids_delete)))

    def _find_objects_to_delete(self):
        pids = []
        current_start = 0
        while True:
            try:
                object_list = self._mn_client.listObjects(
                    start=current_start,
                    count=LIST_OBJECTS_PAGE_SIZE,
                    formatId=LIST_OBJECTS_FORMAT_ID,
                    replicaStatus=False,
                )
            except d1_common.types.exceptions.DataONEException:
                logging.exception('listObjects() failed with exception:')
                raise

            logging.info(
                'Retrieved page: {}/{} ({} objects)'.format(
                    current_start / LIST_OBJECTS_PAGE_SIZE + 1,
                    object_list.total / LIST_OBJECTS_PAGE_SIZE + 1,
                    object_list.count,
                )
            )

            for d1_object in object_list.objectInfo:
                pids.append(d1_object.identifier.value())

            current_start += object_list.count
            if current_start >= object_list.total:
                break
        return pids

    def _delete_objects(self, pids):
        logging.info('Deleting objects on Member Node: {}'.format(self._base_url))
        for pid in pids:
            self._delete_object(pid)

    def _delete_object(self, pid):
        try:
            self._mn_client.delete(pid)
        except d1_common.types.exceptions.DataONEException:
            logging.exception('MNStorage.delete() failed with exception:')
            raise
        else:
            logging.info('Deleted: {}'.format(pid))


if __name__ == '__main__':
    sys.exit(main())
