# ------------------------ IMPORTS ----------------------------- #
import unittest
import requests
import json

# ------------------------ SUITE (ADMIN USERS) ----------------------------- #
class TestAdminUsers(unittest.TestCase):
  def test_list_users(self):
    '''[SUCCESS] You can get the list of users in the system.'''
    response = requests.get(
        'http://localhost:5000/admin/users',
        headers={
          'x-access-token': 'admin' + ' ' + 'admin'
        }
      )
    self.assertTrue(response.status_code == 200)

  def test_success_edit_user(self):
    '''[SUCCESS] You can edit a user in the system'''
    response = requests.put(
        'http://localhost:5000/admin/users/' + "1",
        json={
          'username': 'admin',
          'name': 'new name',
          'last_name': '',
          'role': "admin"
        },
        headers={
          'x-access-token': 'admin' + ' ' + 'admin'
        }
    )
    self.assertTrue(response.status_code == 200)
    self.assertTrue(response.text == "User updated.")

  def test_list_users(self):
    '''[FAIL] You can't get the list of users in the system.'''
    response = requests.get(
        'http://localhost:5000/admin/users',
        headers={
          'x-access-token': 'admin' + ' ' + 'admin'
        }
      )
    self.assertTrue(response.status_code == 200)

  def test_success_edit_user(self):
    '''[FAIL] You can edit a user in the system'''
    response = requests.put(
        'http://localhost:5000/admin/users/' + "1",
        json={
          'username': 'admin',
          'name': 'new name',
          'last_name': '',
          'role': "admin"
        },
        headers={
          'x-access-token': 'admin' + ' ' + 'admin'
        }
    )
    self.assertTrue(response.status_code == 200)
    self.assertTrue(response.text == "User updated.")

  # def test_fail_edit_user_id(self):
  #   '''[FAIL] You can't edit the ID of an user.'''
  #   response = requests.put(
  #     'http://localhost:5000/admin/users/' + "1",
  #       json={
  #         'user-id': 'not-admin',
  #         'username': '',
  #         'name': '',
  #         'last_name': '',
  #         'role': ""
  #       },
  #       headers={
  #         'x-access-token': 'admin' + ' ' + 'admin'
  #       }
  #   )
  #   self.assertTrue(response.status_code == 200)
  #   self.assertTrue(response.text == "User updated.")

  # def test_fail_edit_repeat_username(self):
  #   '''[FAIL] You can't edit the username of a user with another taken user.'''
  #   self.assertTrue(True)

  # def test_success_create_user(self):
  #   '''[SUCCESS] You can create a user for the system.'''
  #   self.assertTrue(True)

  # def test_fail_create_user_repeat_username(self):
  #   '''[FAIL] You can't create a user with a username with another existing user.'''
  #   self.assertTrue(True)

  # def test_fail_create_user_blank_fields(self):
  #   '''[FAIL] You can't create a user with blank username or password'''
  #   self.assertTrue(True)