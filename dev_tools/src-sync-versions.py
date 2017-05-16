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
"""Synchronize the install_requires sections in all setup.py files with the
currently installed versions of all packages.

Only dependencies set to a fixed version ("==") are updated. Dependencies
specified with ">=", "<", etc, remain unchanged.

The two required params are the root to the DataONE Python software stack
and the new version number to use in the next release of the stack. We keep
the version numbers for all the packages in the d1_python repository in sync.
"""

import argparse
import logging
import os
import pkgutil
import re

import d1_common.util
import pkg_resources

import file_iterator
import util


def main():
  parser = argparse.ArgumentParser(
    description='Sync the install_requires sections in setup.py files'
  )
  parser.add_argument('path', help='Root of Python source tree')
  parser.add_argument(
    'd1_version', help='Version to use for new D1 Py stack release'
  )
  parser.add_argument('--exclude', nargs='+', help='Exclude glob patterns')
  parser.add_argument(
    '--no-recursive', dest='recursive', action='store_false', default=True,
    help='Search directories recursively'
  )
  parser.add_argument(
    '--ignore-invalid', action='store_true', default=False,
    help='Ignore invalid paths'
  )
  parser.add_argument(
    '--no-default-excludes', dest='default_excludes', action='store_false',
    default=True, help='Don\'t add default glob exclude patterns'
  )
  parser.add_argument(
    '--debug', action='store_true', default=False, help='Debug level logging'
  )
  parser.add_argument(
    '--diff', dest='diff_only', action='store_true', default=False,
    help='Show diff and do not modify any files'
  )

  args = parser.parse_args()

  d1_common.util.log_setup(args.debug)

  logging.debug('Args:')
  logging.debug('  paths: {}'.format(args.path))
  logging.debug('  exclude: {}'.format(args.exclude))
  logging.debug('  recursive: {}'.format(args.recursive))
  logging.debug('  ignore_invalid: {}'.format(args.ignore_invalid))
  logging.debug('  default_excludes: {}'.format(args.default_excludes))
  logging.debug('  debug: {}'.format(args.debug))
  logging.debug('')

  for setup_path in file_iterator.file_iter(
      path_list=[args.path],
      include_glob_list=['setup.py'],
      exclude_glob_list=args.exclude,
      recursive=args.recursive,
      ignore_invalid=args.ignore_invalid,
      default_excludes=args.default_excludes,
  ):
    update_deps_on_file(setup_path, args.diff_only, args.d1_version)

  update_common_version_const(args.d1_version, args.diff_only)


def update_deps_on_file(setup_path, diff_only, d1_version):
  logging.info('Updating setup.py... path="{}"'.format(setup_path))
  try:
    r = util.redbaron_module_path_to_tree(setup_path)
    r = update_deps_on_tree(r, d1_version)
  except Exception as e:
    logging.error(
      'Dependency update failed. error="{}" path="{}"'.
      format(str(e), setup_path)
    )
    return
  util.update_module_file(r, setup_path, diff_only)


def update_deps_on_tree(r, d1_version):
  dep_node = find_install_requires_node(r)
  for str_node in dep_node.value:
    update_dep_str(str_node, d1_version)
  return r


def find_install_requires_node(r):
  node_list = r('CallArgumentNode')
  for n in node_list:
    if hasattr(n.target, 'value') and n.target.value == 'install_requires':
      return n
  raise UpdateException('install_requires node not found')


def update_dep_str(str_node, d1_version):
  try:
    package_name, old_version_str = parse_dep_str(str_node.value)
  except UpdateException as e:
    logging.debug(
      'Dependency not updated. dep="{}" cause="{}"'.
      format(str_node.value, str(e))
    )
  else:
    new_version_str = get_package_version(package_name, d1_version)
    if old_version_str != new_version_str:
      str_node.value = '\'{} == {}\''.format(package_name, new_version_str)
      logging.debug(
        'Dependency updated. package="{}" old="{}" new="{}"'.
        format(package_name, old_version_str, new_version_str)
      )
    else:
      logging.debug(
        'Dependency update not required. package="{}" version="{}"'.
        format(package_name, old_version_str)
      )


def parse_dep_str(dep_str):
  m = re.match(r'(.*)\s*==\s*(.*)', dep_str)
  if not m:
    raise UpdateException('Dependency not set to fixed version ("==")')
  return m.group(1).strip('\'" '), m.group(2).strip('\'" ')


def get_package_version(package_name, d1_version):
  if package_name.startswith('dataone.'):
    return d1_version
  else:
    return pkg_resources.get_distribution(package_name).version


def update_common_version_const(d1_version, only_diff):
  const_module_path = get_common_const_module_path()
  logging.info(
    'Updating VERSION in d1_common.const. path="{}"'.format(const_module_path)
  )
  r = util.redbaron_module_path_to_tree(const_module_path)
  for n in r('AssignmentNode'):
    if n.target.value == 'VERSION':
      n.value.value = "'{}'".format(d1_version)
      util.update_module_file(r, const_module_path, only_diff)
      break


def get_common_const_module_path():
  return os.path.join(pkgutil.get_loader("d1_common").filename, 'const.py')


class UpdateException(Exception):
  pass


if __name__ == '__main__':
  main()