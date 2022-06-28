# ------------------------ IMPORTS ----------------------------- #
import unittest
import requests
import json

# ------------------------ SUITE (ANALIST USERS) ----------------------------- #
class TestAnalistUsers(unittest.TestCase):
  def test_list_producers(self):
    '''[SUCCESS] You can get the list of producers in the system.'''
    response = requests.get(
        'http://localhost:5000/admin/users',
        headers={
          'x-access-token': 'admin' + ' ' + 'admin'
        }
      )
    self.assertTrue(response.status_code == 200)

  def test_success_edit_producers(self):
    '''[SUCCESS] You can edit a producer in the system'''
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

  def test_list_producers_types(self):
    '''[SUCCESS] You can get the list of producers types in the system.'''
    response = requests.get(
        'http://localhost:5000/admin/users',
        headers={
          'x-access-token': 'admin' + ' ' + 'admin'
        }
      )
    self.assertTrue(response.status_code == 200)

  def test_success_edit_producers_type(self):
    '''[SUCCESS] You can edit a producer type in the system'''
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

  def test_list_producers_types(self):
    '''[FAIL] You can get the list of producers types in the system.'''
    response = requests.get(
        'http://localhost:5000/admin/users',
        headers={
          'x-access-token': 'admin' + ' ' + 'admin'
        }
      )
    self.assertTrue(response.status_code == 200)

  def test_success_edit_producers_type(self):
    '''[FAIL] You can edit a producer type in the system'''
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