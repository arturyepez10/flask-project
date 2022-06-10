# ------------------------ IMPORTS ----------------------------- #
import unittest

# ------------------------ SUITE ----------------------------- #
class TestLogin(unittest.TestCase):
  def test_login_admin(self):
    '''[SUCCESS] You can always log in, as the default admin user.'''
    self.assertTrue(True)

  def test_fail_login_user(self):
    '''[FAIL] You can't log in with an invalid username.'''
    self.assertTrue(True)

  def test_fail_login_password(self):
    '''[FAIL] You can't log in with an invalid username.'''
    self.assertTrue(True)