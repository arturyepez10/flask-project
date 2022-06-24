# ------------------------ IMPORTS ----------------------------- #
# libraries
from flask import Blueprint, render_template, request, make_response, redirect
import requests
import json

# locals
from .routes import routes
from app import db
from database import User, Producer, ProducerType, authorize_required, login_required

# ------------------------ INITIALIZATION ----------------------------- #
# Create the blueprint
analist_bp = Blueprint("analist", __name__)

# ------------------------ VIEWS ----------------------------- #
# Producers lists
@analist_bp.route(routes["analist"]["producers"], methods=['GET', 'POST'])
@login_required
def producers(current_user = None):
  # Variables that the template will use to render
  error = None

  # We obtain all available producers to render them in the list
  all_producers = Producer.query.all()
  
  # We obtain all available producers type
  all_producers_types = ProducerType.query.all()
  if request.method == 'POST':
    # See what action we want to achieve
    if 'action-type' in request.form and request.form['action-type'] == 'create':
      form = request.form

      # We validate if empty fields
      if not (form['name'] and form['last_name'] and form['id_number']):
        error = 'Falta información para enviar la solicitud.'
      else:
        # We make the request to create the producer
        response = requests.post(
          'http://localhost:5000/analist/producers/create',
          json={
            'name': request.form['name'],
            'last_name': request.form['last_name'],
            'id_type': request.form['id_type'],
            'id_number': request.form['id_number'],
            'producer_type': request.form['producer_type'],
            'local_phone': request.form['local_phone'],
            'mobile_phone': request.form['mobile_phone'],
            'address1': request.form['address1'],
            'address2': request.form['address2'],
          },
          headers={
            'x-access-token': current_user['username'] + ' ' + current_user['password']
          }
        )

        # We check what the response was
        if response.status_code == 201:
          all_producers = Producer.query.all()
        else:
          error = response.text
    elif 'edit-producer' in request.form:
      return redirect('/analist' + routes["analist"]["producers"] + '/' + request.form['edit-producer'] + '/details')
    elif 'delete-producer' in request.form:
      # We make the request to eliminate the producer
      response = requests.delete(
        'http://localhost:5000/analist/producers/' + request.form['delete-producer'],
        headers={
          'x-access-token': current_user['username'] + ' ' + current_user['password']
        }
      )

      # We check what the response was
      if response.status_code == 200:
        all_producers = Producer.query.all()
      else:
        error = response.text
  
  return render_template('producers.html', producers=all_producers, producer_types=all_producers_types, error=error)

# Details of a producer
@analist_bp.route(routes["analist"]["producers"] + '/<int:idx>/details', methods=['GET', 'POST'])
@login_required
def producer_details(current_user = None, idx = None):
  if idx is None:
    return redirect('/analista' + routes["analist"]["producers"])

  # We obtain the producer to render it in the details
  producer = Producer.query.filter_by(id=idx).first()

  return render_template('producer-details.html', producer=producer)


# Producers type lists
@analist_bp.route(routes["analist"]["producers-types"], methods=['GET', 'POST'])
@login_required
def producers_types(current_user = None):
  # Variables that the template will use to render
  error = None

  # We obtain all available producers type
  all_producers_types = ProducerType.query.all()

  if request.method == 'POST':
    # See what action we want to achieve
    if 'action-type' in request.form and request.form['action-type'] == 'create':
      # We make the request to create the producer type
      response = requests.post(
        'http://localhost:5000/analist/producers/types/create',
        json={
          'name': request.form['name'],
        },
        headers={
          'x-access-token': current_user['username'] + ' ' + current_user['password']
        }
      )

      # We check what the response was
      if response.status_code == 201:
        all_producers_types = ProducerType.query.all()
      else:
        error = response.text
    elif 'edit-producer-type' in request.form:
      pass
    elif 'delete-producer-type' in request.form:
      # We make the request to delete the producer type
      response = requests.delete(
        'http://localhost:5000/analist/producers/types/' + request.form['delete-producer-type'],
        headers={
          'x-access-token': current_user['username'] + ' ' + current_user['password']
        }
      )

      # We check what the response was
      if response.status_code == 200:
        all_producers_types = ProducerType.query.all()
      else:
        error = response.text

  return render_template('producer-type.html', producer_types=all_producers_types, error=error)



# ------------------------ CONTROLLERS ----------------------------- #
# Create Producer
@analist_bp.route(routes["analist"]["producers"] + '/create', endpoint="create-producer", methods=['POST'])
@authorize_required
def create_producer_type():
  # Parse the answeer from the request
  data = json.loads(request.data)

  # We check the body of the response
  if not ('name' in data and 'last_name' in data and 'producer_type' in data and 'id_number' in data):
    return make_response('Not enough information to create a producer.', 400)
  else:
    # We find the producer type if it exists
    producer_type = ProducerType.query.filter_by(name=data['producer_type']).first()

    if producer_type is None:
      return make_response('Producer type not found.', 404)

    # New producer
    producer = Producer(
      id_type=data['id_type'],
      id_number=data['id_number'],
      name=data['name'],
      last_name=data['last_name'],
      producer_type_id=producer_type.id,
      local_phone=data['local_phone'],
      mobile_phone=data['mobile_phone'],
      address1=data['address1'],
      address2=data['address2'],
    )
    
    # We commit the changes to the database
    db.session.add(producer)
    db.session.commit()

    return make_response('Producer created.', 201)

# Edit Producer
@analist_bp.route(routes["analist"]["producers"] + '/<int:idx>/edit', endpoint="edit-producer", methods=['PUT'])
@authorize_required
def edit_producer_type(idx):
  # We check if the producer exists
  producer = Producer.query.filter_by(id=idx).first()

  if producer is None:
    return make_response('Producer not found.', 404)
  
  # Parse the answeer from the request
  data = json.loads(request.data)

  # Update the producer according
  if data['id_type']:
    producer.id_type = data['id_type']
  if data['id_number']:
    producer.id_number = data['id_number']
  if data['name']:
    producer.name = data['name']
  if data['last_name']:
    producer.last_name= data['last_name']
  if data['producer_type']:
    producer_type = ProducerType.query.filter_by(name=data['producer_type']).first()

    if producer_type is None:
      return make_response('Producer type not found.', 404)

    producer.producer_type_id = producer_type.id
  if data['local_phone']:
    producer.local_phone = data['local_phone']
  if data['mobile_phone']:
    producer.mobile_phone = data['mobile_phone']
  if data['address1']:
    producer.address1 = data['address1']
  
  # We commit the changes to the database
  db.session.commit()

  return make_response('Producer updated.', 200)

# Delete producer
@analist_bp.route(routes["analist"]["producers"] + '/<int:idx>', endpoint="delete-producer", methods=['DELETE'])
@authorize_required
def delete_producer(idx):
  # We check if the producer exists
  producer = Producer.query.filter_by(id=idx).first()

  if producer is None:
    return make_response('Producer not found.', 404)

  # We delete the producer
  db.session.delete(producer)
  db.session.commit()

  return make_response('Producer deleted.', 200)

# Create Producer Type
@analist_bp.route(routes["analist"]["producers-types"] + '/create', endpoint="create-producer-type", methods=['POST'])
@authorize_required
def create_producer_type():
  # Parse the answeer from the request
  data = json.loads(request.data)

  # We check the body of the response
  if 'name' not in data:
    return make_response('No name for the producer type', 404)
  else:
    # new producer type
    producer_type = ProducerType(name=data['name'])
    
    # We commit the changes to the database
    db.session.add(producer_type)
    db.session.commit()

    return make_response('Producer type created.', 201)

# Delete Producer Type
@analist_bp.route(routes["analist"]["producers-types"] + '/<int:idx>', endpoint="delete-producer-type", methods=['DELETE'])
@authorize_required
def create_producer_type(idx):
  # We obtain the producer type to delete
  producer_type = ProducerType.query.filter_by(id=idx).first()

  # We check the body of the response
  if producer_type is None:
    return make_response('There is no producer type by that id.', 404)
  else:
    # eliminate producer type
    ProducerType.query.filter_by(id=idx).delete()
    
    # We commit the changes to the database
    db.session.commit()

    return make_response('Producer type deleted.', 200)