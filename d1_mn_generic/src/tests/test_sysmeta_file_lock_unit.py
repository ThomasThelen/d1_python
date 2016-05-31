__author__ = 'mark'

import unittest
import service.mn.management.commands.process_system_metadata_refresh_queue as sysmeta_rep_queue
import os
import subprocess
import fcntl
import tempfile
from mock import patch, PropertyMock
import django
from django.core.management.base import NoArgsCommand

# import tempfile


class SysMetaRefresher():
  def __init__(self):
    pass

  def process_refresh_queue(self):
    pass


class TestFileLockUnit(unittest.TestCase):
  # django.setup()
  def setUp(self):
    self.lock_file = '/home/mark/d1/d1_python/d1_mn_generic/src/tests/test_file_lock_unit.single'

  def tearDown(self):
    try:
      os.remove(self.lock_file)
    except:
      pass

  #---------------------------------------------
  def test_process_queue_acquire_lock(self):
    lock_name = '/home/mark/d1/d1_python/d1_mn_generic/src/tests/test_file_lock_unit.single'
    rp = sysmeta_rep_queue.Command()
    rp._acquire()
    new_rep_lock = sysmeta_rep_queue.Command()
    try:
      new_rep_lock._acquire()
    except IOError, e:
      print e.errno
    self.assertEqual(e.errno, 11)

  def test_process_queue_release_lock(self):
    lock_name = '/home/mark/d1/d1_python/d1_mn_generic/src/tests/test_file_lock_unit.single'
    rp = sysmeta_rep_queue.Command()
    rp._acquire()
    new_rep_lock = sysmeta_rep_queue.Command()
    file_locked = True
    rp._release()
    try:
      new_rep_lock._acquire()
      file_locked = False
    except IOError, e:
      print e.errno
    self.assertFalse(file_locked)

  def test_acquire_assert_called_flock(self):
    with patch(
      'service.mn.management.commands.process_system_metadata_refresh_queue.fcntl.flock'
    ) as mocked_method:
      lock_name = '/home/mark/d1/d1_python/d1_mn_generic/src/tests/test_file_lock_unit.single'
      sng = sysmeta_rep_queue.Command()
      sng._acquire()
      mocked_method.assert_called_with(sng.file_handle, 6)

  @patch(
    'service.mn.management.commands.process_system_metadata_refresh_queue.SysMetaRefresher.process_system_metadata_refresh_queue'
  )
  @patch(
    'service.mn.management.commands.process_system_metadata_refresh_queue.SysMetaRefresher'
  )
  def test_process_queue(self, mock_proc, mock_queue):
    with patch(
      'service.mn.management.commands.process_system_metadata_refresh_queue.sys.exit'
    ) as mock_exit:
      lock_name = '/home/mark/d1/d1_python/d1_mn_generic/src/tests/test_file_lock_unit.single'
      sng = sysmeta_rep_queue.Command()
      sng._acquire()
      new_sng = sysmeta_rep_queue.Command()
      try:
        new_sng.handle_noargs()
      except IOError, e:
        print e.errno
      self.assertFalse(new_sng.locked)

  @patch(
    'service.mn.management.commands.process_system_metadata_refresh_queue.SysMetaRefresher.process_system_metadata_refresh_queue'
  )
  @patch(
    'service.mn.management.commands.process_system_metadata_refresh_queue.SysMetaRefresher'
  )
  @patch(
    'service.mn.management.commands.process_system_metadata_refresh_queue.Command._abort_if_stand_alone_instance'
  )
  @patch(
    'service.mn.management.commands.process_system_metadata_refresh_queue.Command._log_setup'
  )
  def test_handle_noargs_called_abort(
    self, mock_log, mock_abort, mock_init, mock_process
  ):
    with patch(
      'service.mn.management.commands.process_system_metadata_refresh_queue.Command._get_lock',
      new_callable=PropertyMock
    ) as mocked_method:
      cmd = sysmeta_rep_queue.Command()
      mock_init.return_value = SysMetaRefresher()
      cmd.handle_noargs()
      mocked_method.assert_called_with()

  @patch(
    'service.mn.management.commands.process_system_metadata_refresh_queue.SysMetaRefresher.process_system_metadata_refresh_queue'
  )
  @patch(
    'service.mn.management.commands.process_system_metadata_refresh_queue.SysMetaRefresher'
  )
  @patch(
    'service.mn.management.commands.process_system_metadata_refresh_queue.Command._get_lock'
  )
  @patch(
    'service.mn.management.commands.process_system_metadata_refresh_queue.Command._log_setup'
  )
  def test_handle_noargs_called_abort_if_stand_alone_instance(
    self, mock_log, mock_abort, mock_init, mock_process
  ):
    with patch(
      'service.mn.management.commands.process_system_metadata_refresh_queue.Command._abort_if_stand_alone_instance',
      new_callable=PropertyMock
    ) as mocked_method:
      cmd = sysmeta_rep_queue.Command()
      mock_init.return_value = SysMetaRefresher()
      cmd.handle_noargs()
      mocked_method.assert_called_with()

  @patch(
    'service.mn.management.commands.process_system_metadata_refresh_queue.Command._abort_if_stand_alone_instance'
  )
  @patch(
    'service.mn.management.commands.process_system_metadata_refresh_queue.SysMetaRefresher.process_system_metadata_refresh_queue'
  )
  @patch(
    'service.mn.management.commands.process_system_metadata_refresh_queue.SysMetaRefresher'
  )
  @patch(
    'service.mn.management.commands.process_system_metadata_refresh_queue.Command._log_setup'
  )
  def test_handle_noargs_lock_acquired(
    self, mock_log, mock_init, mock_process, mock_abort
  ):
    cmd = sysmeta_rep_queue.Command()
    mock_init.return_value = SysMetaRefresher()
    cmd.handle_noargs()
    self.assertEqual(
      cmd.filename, os.path.join(
        os.path.dirname(
          os.path.dirname(
            __file__
          )
        ), 'service', 'mn', 'management', 'commands',
        'process_system_metadata_refresh_queue.single'
      )
    )


if __name__ == '__main__':
  unittest.main()
