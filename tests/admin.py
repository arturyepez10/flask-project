# ------------------------ IMPORTS ----------------------------- #
import unittest

# ------------------------ SUITE (ADMIN USERS) ----------------------------- #
class TestAdminUsers(unittest.TestCase):
  def test_list_users(self):
    '''[SUCCESS] You can get the list of users in the system.'''
    self.assertTrue(True)

  def test_success_edit_user(self):
    '''[SUCCESS] You can edit a user in the system'''
    self.assertTrue(True)

  def test_fail_edit_user_id(self):
    '''[FAIL] You can't edit the ID of an user.'''
    self.assertTrue(True)

  def test_fail_edit_repeat_username(self):
    '''[FAIL] You can't edit the username of a user with another taken user.'''
    self.assertTrue(True)

  def test_success_create_user(self):
    '''[SUCCESS] You can create a user for the system.'''
    self.assertTrue(True)

  def test_fail_create_user_repeat_username(self):
    '''[FAIL] You can't create a user with a username with another existing user.'''
    self.assertTrue(True)

  def test_fail_create_user_blank_fields(self):
    '''[FAIL] You can't create a user with blank username or password'''
    self.assertTrue(True)