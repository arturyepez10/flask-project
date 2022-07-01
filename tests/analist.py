# ------------------------ IMPORTS ----------------------------- #
import unittest
import requests
import json

# ------------------------ SUITE (ANALIST USERS) ----------------------------- #
class TestAnalistUsers(unittest.TestCase):
  def test_list_producers(self):
    '''[SUCCESS] You can get the list of producers in the system.'''
    response = requests.get(
      'http://localhost:5000/analist/producers',
      headers={
        'x-access-token': 'admin' + ' ' + 'admin'
      }
    )
    self.assertTrue(response.status_code == 200)

  def test_success_create_producer_type(self):
    '''[SUCCESS] You can create a producer type in the system'''
    response = requests.post(
      'http://localhost:5000/analist/producers/types/create',
      json={
        'name': 'unique producer type',
      },
      headers={
        'x-access-token': 'admin' + ' ' + 'admin'
      }
    )
    self.assertTrue(response.status_code == 201)
    self.assertTrue(response.text == "Producer type created.")

  def test_failure_create_producer_type(self):
    '''[FAIL] You can create a producer type without name in the system'''
    response = requests.post(
      'http://localhost:5000/analist/producers/types/create',
      json={
        'noname': '',
      },
      headers={
        'x-access-token': 'admin' + ' ' + 'admin'
      }
    )
    self.assertTrue(response.status_code == 404)
    self.assertTrue(response.text == "No name for the producer type.")

  def test_success_delete_producer_type(self):
    '''[SUCCESS] You can delete a producer type in the system'''
    create_response = requests.post(
      'http://localhost:5000/analist/producers/types/create',
      json={
        'name': 'producer to delete',
      },
      headers={
        'x-access-token': 'admin' + ' ' + 'admin'
      }
    )
    self.assertTrue(create_response.status_code == 201)
    delete_response = requests.delete(
      'http://localhost:5000/analist/producers/types/2',
      headers={
        'x-access-token': 'admin' + ' ' + 'admin'
      }
    )
    self.assertTrue(delete_response.status_code == 200)
    self.assertTrue(delete_response.text == "Producer type id deleted.")

  def test_failure_delete_producer_type(self):
    '''[FAIL] You can delete a producer type that doesn't exist in the system'''
    delete_response = requests.delete(
      'http://localhost:5000/analist/producers/types/20000',
      headers={
        'x-access-token': 'admin' + ' ' + 'admin'
      }
    )
    self.assertTrue(delete_response.status_code == 404)
    self.assertTrue(delete_response.text == "There is no producer type by that id.")

  def test_list_producers_types(self):
    '''[SUCCESS] You can get the list of producers types in the system.'''
    response = requests.get(
        'http://localhost:5000/analist/producers/types',
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

  def test_success_create_producer(self):
    '''[SUCCESS] You can create a producer in the system'''
    create_producer_type_response = requests.post(
      'http://localhost:5000/analist/producers/types/create',
      json={
        'name': 'unique producer type',
      },
      headers={
        'x-access-token': 'admin' + ' ' + 'admin'
      }
    )
    self.assertTrue(create_producer_type_response.status_code == 201)
    response = requests.post(
      'http://localhost:5000/analist/producers/create',
      json={
        'id_type': 'V',
        'id_number': 1234565,
        'name': 'producer name',
        'last_name': 'producer last name',
        'producer_type': 'unique producer type',
        'local_phone': '12345',
        'mobile_phone': '12345',
        'address1': 'asfasfasf',
        'address2': 'asfasfaf'
      },
      headers={
        'x-access-token': 'admin' + ' ' + 'admin'
      }
    )
    self.assertTrue(response.status_code == 201)
    self.assertTrue(response.text == "Producer created.")
  
  def test_failure_create_producer_v1(self):
    '''[FAIL] You can create a producer without name, last_name, producer_type, id_type or id_number in the system'''
    response = requests.post(
      'http://localhost:5000/analist/producers/create',
      json={
        'local_phone': '12345',
        'mobile_phone': '12345',
        'address1': 'asfasfasf',
        'address2': 'asfasfaf'
      },
      headers={
        'x-access-token': 'admin' + ' ' + 'admin'
      }
    )
    self.assertTrue(response.status_code == 400)
    self.assertTrue(response.text == "Not enough information to create a producer.")

  def test_failure_create_producer_v2(self):
    '''[FAIL] You can create a producer with a invalid producer type in the system'''
    create_producer_type_response = requests.post(
      'http://localhost:5000/analist/producers/types/create',
      json={
        'name': 'unique producer type',
      },
      headers={
        'x-access-token': 'admin' + ' ' + 'admin'
      }
    )
    self.assertTrue(create_producer_type_response.status_code == 201)
    response = requests.post(
      'http://localhost:5000/analist/producers/create',
      json={
        'id_type': 'V',
        'id_number': 1234565,
        'name': 'producer name',
        'last_name': 'producer last name',
        'producer_type': 'invalid producer type',
        'local_phone': '12345',
        'mobile_phone': '12345',
        'address1': 'asfasfasf',
        'address2': 'asfasfaf'
      },
      headers={
        'x-access-token': 'admin' + ' ' + 'admin'
      }
    )
    self.assertTrue(response.status_code == 404)
    self.assertTrue(response.text == "Producer type not found.")

  def test_success_delete_producer(self):
    '''[SUCCESS] You can delete a producer in the system'''
    create_producer_type_response = requests.post(
      'http://localhost:5000/analist/producers/types/create',
      json={
        'name': 'unique producer type 2',
      },
      headers={
        'x-access-token': 'admin' + ' ' + 'admin'
      }
    )
    self.assertTrue(create_producer_type_response.status_code == 201)
    create_producer_response = requests.post(
      'http://localhost:5000/analist/producers/create',
      json={
        'id_type': 'V',
        'id_number': 1234565,
        'name': 'producer name',
        'last_name': 'producer last name',
        'producer_type': 'unique producer type 2',
        'local_phone': '12345',
        'mobile_phone': '12345',
        'address1': 'asfasfasf',
        'address2': 'asfasfaf'
      },
      headers={
        'x-access-token': 'admin' + ' ' + 'admin'
      }
    )
    self.assertTrue(create_producer_response.status_code == 201)
    self.assertTrue(create_producer_response.text == "Producer created.")
    delete_producer_response = requests.delete(
      'http://localhost:5000/analist/producers/1',
      headers={
        'x-access-token': 'admin' + ' ' + 'admin'
      }
    )
    self.assertTrue(delete_producer_response.status_code == 200)
    self.assertTrue(delete_producer_response.text == "Producer deleted.")

  def test_failure_delete_producer(self):
    '''[FAIL] You can delete a nonexist producer in the system'''
    delete_producer_response = requests.delete(
      'http://localhost:5000/analist/producers/100',
      headers={
        'x-access-token': 'admin' + ' ' + 'admin'
      }
    )
    self.assertTrue(delete_producer_response.status_code == 404)
    self.assertTrue(delete_producer_response.text == "Producer not found.")

  def test_success_edit_producer(self):
    '''[SUCCESS] You can edit a producer in the system'''
    create_producer_type_response = requests.post(
      'http://localhost:5000/analist/producers/types/create',
      json={
        'name': 'unique producer type 3',
      },
      headers={
        'x-access-token': 'admin' + ' ' + 'admin'
      }
    )
    self.assertTrue(create_producer_type_response.status_code == 201)
    create_producer_response = requests.post(
      'http://localhost:5000/analist/producers/create',
      json={
        'id_type': 'V',
        'id_number': 1234565,
        'name': 'edit producer name',
        'last_name': 'producer last name',
        'producer_type': 'unique producer type 3',
        'local_phone': '12345',
        'mobile_phone': '12345',
        'address1': 'asfasfasf',
        'address2': 'asfasfaf'
      },
      headers={
        'x-access-token': 'admin' + ' ' + 'admin'
      }
    )
    self.assertTrue(create_producer_response.status_code == 201)
    self.assertTrue(create_producer_response.text == "Producer created.")
    edit_producer_response = requests.put(
      'http://localhost:5000/analist/producers/2',
      json={
        'id_type': 'V',
        'id_number': 1234565,
        'name': 'new edit producer name',
        'last_name': 'producer last name',
        'producer_type': 'unique producer type 3',
        'local_phone': '12345',
        'mobile_phone': '12345',
        'address1': 'asfasfasf',
        'address2': 'asfasfaf'
      },
      headers={
        'x-access-token': 'admin' + ' ' + 'admin'
      }
    )
    self.assertTrue(edit_producer_response.status_code == 200)
    self.assertTrue(edit_producer_response.text == "Producer updated.")

  def test_failure_edit_producer(self):
    '''[FAIL] You can edit a nonexist producer in the system'''
    edit_producer_response = requests.put(
      'http://localhost:5000/analist/producers/200',
      json={
        'id_type': 'V',
        'id_number': 1234565,
        'name': 'new edit producer name',
        'last_name': 'producer last name',
        'producer_type': 'unique producer type 3',
        'local_phone': '12345',
        'mobile_phone': '12345',
        'address1': 'asfasfasf',
        'address2': 'asfasfaf'
      },
      headers={
        'x-access-token': 'admin' + ' ' + 'admin'
      }
    )
    self.assertTrue(edit_producer_response.status_code == 404)
    self.assertTrue(edit_producer_response.text == "Producer not found.")