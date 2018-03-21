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
"""URL to view mapping
"""

import d1_gmn.app.views.diag
import d1_gmn.app.views.ext
import d1_gmn.app.views.external
import d1_gmn.app.views.get_package
import d1_gmn.app.views.internal

import django.conf.urls as urls

urlpatterns = [
  # Django's URL dispatcher does not take HTTP verb into account, so in the
  # cases where the DataONE REST API specifies different methods as different
  # verbs against the same URL, the methods are dispatched to the same view
  # function, which checks the verb and dispatches to the appropriate handler.

  # Tier 1: Core API (MNCore)
  # MNCore.ping() - GET /monitor/ping
  urls.url(
    r'^v[12]/monitor/ping/?$',
    d1_gmn.app.views.external.get_monitor_ping,
    name='get_monitor_ping',
  ),
  # MNCore.getLogRecords() - GET /log
  urls.url(
    r'^v[12]/log/?$',
    d1_gmn.app.views.external.get_log,
    name='get_log',
  ),
  # MNCore.getCapabilities() - GET /node
  # Also available via Apache redirect from /
  urls.url(
    r'^v[12]/?$',
    d1_gmn.app.views.external.get_node,
    name='get_node',
  ),
  urls.url(
    r'^v[12]/node/?$',
    d1_gmn.app.views.external.get_node,
    name='get_node',
  ),

  # Tier 1: Read API (MNRead)
  # MNRead.get() - GET /object/{did}
  urls.url(
    r'^v[12]/object/(.+)$',
    d1_gmn.app.views.external.dispatch_object,
    name='dispatch_object',
  ),
  # MNRead.getSystemMetadata() - GET /meta/{did}
  urls.url(
    r'^v[12]/meta/(.+)$',
    d1_gmn.app.views.external.get_meta,
    name='get_meta',
  ),
  # MNStorage.updateSystemMetadata() - PUT /meta
  urls.url(
    r'^v2/meta$',
    d1_gmn.app.views.external.put_meta,
    name='put_meta',
  ),
  # MNRead.describe() - HEAD /object/{did}
  # (handled by object dispatcher)
  # MNRead.getChecksum() - GET /checksum/{did}
  urls.url(
    r'^v[12]/checksum/(.+)$',
    d1_gmn.app.views.external.get_checksum,
    name='get_checksum',
  ),
  # MNRead.listObjects() - GET /object
  urls.url(
    r'^v[12]/object/?$',
    d1_gmn.app.views.external.dispatch_object_list,
    name='dispatch_object_list',
  ),
  # MNRead.synchronizationFailed() - POST /error
  urls.url(
    r'^v[12]/error/?$',
    d1_gmn.app.views.external.post_error,
    name='post_error',
  ),
  # MNRead.getReplica() - GET /replica/{did}
  urls.url(
    r'^v[12]/replica/(.+)/?$',
    d1_gmn.app.views.external.get_replica,
    name='get_replica',
  ),

  # Tier 2: Authorization API  (MNAuthorization)
  # MNAuthorization.isAuthorized() - GET /isAuthorized/{did}
  urls.url(
    r'^v[12]/isAuthorized/(.+)/?$',
    d1_gmn.app.views.external.get_is_authorized,
    name='get_is_authorized',
  ),
  # MNStorage.systemMetadataChanged() - POST /refreshSystemMetadata/{did}
  urls.url(
    r'^v[12]/dirtySystemMetadata/?$',
    d1_gmn.app.views.external.post_refresh_system_metadata,
    name='post_refresh_system_metadata',
  ),

  # Tier 3: Storage API (MNStorage)
  # MNStorage.create() - POST /object
  # (handled by object dispatcher)
  # MNStorage.update() - PUT /object/{did}
  # (handled by object dispatcher)
  # MNStorage.generateIdentifier()
  urls.url(
    r'^v[12]/generate/?$',
    d1_gmn.app.views.external.post_generate_identifier,
    name='post_generate_identifier',
  ),
  # MNStorage.delete() - DELETE /object/{did}
  # (handled by object dispatcher)
  # MNStorage.archive() - PUT /archive/{did}
  urls.url(
    r'^v[12]/archive/(.+)/?$',
    d1_gmn.app.views.external.put_archive,
    name='put_archive',
  ),
  # Tier 4: Replication API (MNReplication)
  # MNReplication.replicate() - POST /replicate
  urls.url(
    r'^v[12]/replicate/?$',
    d1_gmn.app.views.external.post_replicate,
    name='post_replicate',
  ),
  # Package API
  # MNPackage.getPackage() - GET /package
  urls.url(
    r'^v2/packages/(?P<package_type>.+)/(?P<pid>.+)/?$',
    d1_gmn.app.views.get_package.get_package,
    name='get_package',
  ),

  #
  # Home page and Web UI
  #
  urls.url(r'^home/?$', d1_gmn.app.views.internal.home, name='home'),
  # url(
  #   r'^home/replication?$', d1_gmn.app.views.internal.replication_queue,
  #   name='home_replication'
  # ),
  # Environment (discovered CNs, etc))
  # url(
  #   r'^home/env',
  #   d1_gmn.app.views.home.d1env,
  #   name='d1env',
  # ),

  #
  # GMN API extensions
  #
  urls.url(
    r'^ext/object/?$',
    d1_gmn.app.views.ext.get_object_list_json,
    name='get_object_list_json',
  ),

  #
  # GMN diagnostic APIs
  #
  urls.url(
    r'^diag/echo-session/?$',
    d1_gmn.app.views.diag.echo_session,
    name='echo_session',
  ),
  urls.url(
    r'^diag/echo-request/?$',
    d1_gmn.app.views.diag.echo_request,
    name='echo_request_object',
  ),
  urls.url(
    r'^diag/echo-exception/(.+?)$', d1_gmn.app.views.diag.echo_exception,
    name='echo_exception'
  ),
]
