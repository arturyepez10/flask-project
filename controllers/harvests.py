# ------------------------ IMPORTS ----------------------------- #
# libraries
from flask import Blueprint, render_template, request, make_response, redirect
import sqlalchemy as sa
import requests
import json

# locals
from .routes import routes
from app import db
from database import Harvest, Purchase, Product, authorize_required, login_required

# ------------------------ INITIALIZATION ----------------------------- #
# Create the blueprint
harvests_bp = Blueprint("harvests", __name__)

# ------------------------ VIEWS ----------------------------- #
# Harvests lists
@harvests_bp.route(routes["harvests"]["portfolio"], methods=["GET", "POST"])
@login_required
def harvests(current_user = None):
  # Variables that the template will use to render
  error = None

  # Get all the harvests from the database
  harvests = Harvest.query.all()

  if request.method == 'POST':
    # See what action we want to achieve
    if 'action-type' in request.form and request.form['action-type'] == 'create':
      form = request.form

      # We validate empty fields
      if not (form['description'] and form['beginning'] and form['closure']):
        error = 'Falta información para enviar la solicitud.'
      else:
        # We make the request to create the harvest
        response = requests.post(
          'http://localhost:5000/analyst/harvests/create',
          json={
            'description': request.form['description'],
            'beginning': request.form['beginning'],
            'closure': request.form['closure'],
          },
          headers={
            'x-access-token': current_user['username'] + ' ' + current_user['password']
          }
        )

        # We check what the response was
        if response.status_code == 201:
          harvests = Harvest.query.all()
        else:
          error = response.text
    
    elif 'edit-harvest' in request.form:
      return redirect('/analyst' + routes["harvests"]["portfolio"] + '/' + request.form['edit-harvest'] + '/details')

    elif 'delete-harvest' in request.form:
      # We delete the harvest
      response = requests.delete(
        'http://localhost:5000/analyst/harvests/' + request.form['delete-harvest'],
        headers={
          'x-access-token': current_user['username'] + ' ' + current_user['password']
        }
      )

      # We check what the response was
      if response.status_code == 200:
        harvests = Harvest.query.all()
      else:
        error = response.text

  return render_template("harvests.html", harvests=harvests, error=error), 200

# Details of a harvest
@harvests_bp.route(routes["harvests"]["portfolio"] + '/<int:idx>/details', methods=['GET', 'POST'])
@login_required
def harvest_details(idx, current_user = None):
  # Variables that the template will use to render
  error = None

  # Get the harvest from the database
  harvest = Harvest.query.filter_by(id=idx).first()

  if request.method == 'POST':
    # See what action we want to achieve
    if 'edit-harvest' in request.form:
      pass

    elif 'delete-harvest' in request.form:
      # We delete the harvest
      response = requests.delete(
        'http://localhost:5000/analyst/harvests/' + str(idx),
        headers={
          'x-access-token': current_user['username'] + ' ' + current_user['password']
        }
      )

      # We check what the response was
      if response.status_code == 200:
        return redirect('/analyst' + routes["harvests"]["portfolio"])
      else:
        error = response.text

    elif 'list-purchases' in request.form:
      # We verify if the harvest have associated purchase
      if harvest.purchase is not None:
        return redirect('/analyst' + routes["harvests"]["portfolio"] + '/' + str(idx) + '/purchase')

    elif 'generate-purchase' in request.form:
      # We verify if the harvest have associated purchase
      if harvest.purchase is not None:
        return redirect('/analyst' + routes["harvests"]["portfolio"] + '/' + str(idx) + '/purchase')
      else:
        # We generate the purchase
        response = requests.post(
          'http://localhost:5000/analyst/purchases/create',
          json={
            'harvest': idx,
          },
          headers={
            'x-access-token': current_user['username'] + ' ' + current_user['password']
          }
        )

        # We check what the response was
        if response.status_code == 201:
          return redirect('/analyst' + routes["harvests"]["portfolio"] + '/' + str(idx) + '/purchase')
        else:
          error = response.text

    elif 'enable-harvest' in request.form:
      # We edit the harvest
      response = requests.put(
        'http://localhost:5000/analyst/harvests/' + str(idx),
        json={
          'state': 'active',
        },
        headers={
          'x-access-token': current_user['username'] + ' ' + current_user['password']
        }
      )

      # We check what the response was
      if response.status_code == 200:
        return redirect('/analyst' + routes["harvests"]["portfolio"])
      else:
        error = response.text
    
    elif 'disable-harvest' in request.form:
      # We edit the harvest
      response = requests.put(
        'http://localhost:5000/analyst/harvests/' + str(idx),
        json={
          'state': 'inactive',
        },
        headers={
          'x-access-token': current_user['username'] + ' ' + current_user['password']
        }
      )

      # We check what the response was
      if response.status_code == 200:
        return redirect('/analyst' + routes["harvests"]["portfolio"])
      else:
        error = response.text

  return render_template("harvests-details.html", harvest=harvest, error=error), 200

# Purchase of a harvest
@harvests_bp.route(routes["harvests"]["portfolio"] + '/<int:idx>/purchase', methods=['GET', 'POST'])
@login_required
def harvest_purchase(idx, current_user = None):
  # Variables that the template will use to render
  error = None

  # Get the harvest from the database
  harvest = Harvest.query.filter_by(id=idx).first()
  harvest_products = harvest.purchase.products_list

  if request.method == 'POST':
    if 'action-type' in request.form and request.form['action-type'] == 'create':
      # We make the request to create the harvest
      response = requests.post(
        'http://localhost:5000/analyst/purchases/' + str(idx) + '/add-product',
        json={
          'id_type': request.form['id_type'],
          'id_number': request.form['id_number'],
          'name': request.form['name'],
          'price': request.form['price'],
          'qty': request.form['qty'],
          'date': request.form['date'],
          'humidity': request.form['humidity'],
          'depletion': request.form['depletion'],
          'total_qty': request.form['total_qty'],
          'amount': request.form['amount'],
          'description': request.form['description'],
        },
        headers={
          'x-access-token': current_user['username'] + ' ' + current_user['password']
        }
      )

      # We check what the response was
      if response.status_code == 201:
        return redirect('/analyst' + routes["harvests"]["portfolio"] + '/' + str(idx) + '/purchase')
      else:
        error = response.text

    elif 'delete-product' in request.form:
      # We make the request to delete the product
      response = requests.delete(
        'http://localhost:5000/analyst/purchases/' + str(idx) + '/product/' + request.form['delete-product'],
        headers={
          'x-access-token': current_user['username'] + ' ' + current_user['password']
        }
      )

      # We check what the response was
      if response.status_code == 200:
        return redirect('/analyst' + routes["harvests"]["portfolio"] + '/' + str(idx) + '/purchase')
      else:
        error = response.text

  return render_template("harvest-purchase.html", harvest=harvest, products= harvest_products, error=error), 200

# List of purchases
@harvests_bp.route(routes["harvests"]["purchases"], methods=['GET', 'POST'])
@login_required
def purchases(current_user = None):
  # Variables that the template will use to render
  error = None

  # We obtain all purchases
  all_purchases = Purchase.query.all()

  if request.method == 'POST':
    if 'view-details' in request.form:
      return redirect('/analyst' + routes["harvests"]["portfolio"] + '/' + request.form['view-details'] + '/purchase')

  return render_template('purchases.html', purchases=all_purchases, error=error), 200


# ------------------------ CONTROLLERS ----------------------------- #
# Create Harvest
@harvests_bp.route(routes["harvests"]["portfolio"] + '/create', endpoint="create-harvest", methods=['POST'])
@authorize_required
def create_harvest():
  # Parse the answeer from the request
  data = json.loads(request.data)

  # We check the body of the response
  if not ('description' in data and 'beginning' in data and 'closure' in data):
    return make_response('No existe descripcion o fechas para la cosecha.', 404)
  else:
    # new harvest
    harvest = Harvest(
      description=data['description'],
      beginning=data['beginning'],
      closure=data['closure'],
      state="active"
    )
    
    # We commit the changes to the database
    db.session.add(harvest)
    db.session.commit()

    return make_response('Harvest created.', 201)

# Edit Harvest
@harvests_bp.route(routes["harvests"]["portfolio"] + '/<int:idx>', endpoint="edit-harvest", methods=['PUT'])
@authorize_required
def edit_harvest(idx):
  # Parse the answeer from the request
  data = json.loads(request.data)

  # We get the harvest from the database
  harvest = Harvest.query.filter_by(id=idx).first()
  
  # We check if the harvest exists
  if harvest is None:
    return make_response('No existe cosecha.', 404)
  else:

    # We update the harvest
    if 'description' in data:
      harvest.description = data['description']
    if 'beginning' in data:
      harvest.beginning = data['beginning']
    if 'closure' in data:
      harvest.closure = data['closure']
    if 'state' in data:
      harvest.state = data['state']

    # We commit the changes to the database
    db.session.commit()

    return make_response('Harvest updated.', 200)

# Delete Harvest
@harvests_bp.route(routes["harvests"]["portfolio"] + '/<int:idx>', endpoint="delete-harvest", methods=['DELETE'])
@authorize_required
def delete_harvest(idx):
  # We get the harvest from the database
  harvest = Harvest.query.filter_by(id=idx).first()

  # We check if the harvest exists
  if harvest is None:
    return make_response('No existe cosecha.', 404)
  else:
    # We verify if there is purchase and products, to delete them first
    if harvest.purchase is not None:
      # We delete the products first
      if harvest.purchase.products is not None:
        for product in harvest.purchase.products:
          db.session.delete(product)

      # We delete the purchase
      db.session.delete(harvest.purchase)

    # We delete the harvest
    db.session.delete(harvest)
    db.session.commit()

    return make_response('Harvest deleted.', 200)

# Create purchase
@harvests_bp.route(routes["harvests"]["purchases"] + '/create', endpoint="create-purchase", methods=['POST'])
@authorize_required
def create_purchase():
  # Parse the answeer from the request
  data = json.loads(request.data)

  # We check the body of the response
  if not ('harvest' in data):
    return make_response('No se encuentra cosecha.', 404)
  else:
    # new purchase
    purchase = Purchase(
      total_price=0.0,
      item_qty=0
    )
    db.session.add(purchase)
    
    # We find the harvest
    harvest = Harvest.query.filter_by(id=data['harvest']).first()

    if harvest is None:
      return make_response('No existe cosecha.', 404)

    # We add the purchase to the harvest
    harvest.purchase_id = purchase.id

    # We commit the changes to the database
    db.session.commit()

    return make_response('Purchase created.', 201)

# Add product to purchase
@harvests_bp.route(routes["harvests"]["purchases"] + '/<int:idx>/add-product', endpoint="add-product", methods=['POST'])
@authorize_required
def add_product(idx):
  # Parse the answeer from the request
  data = json.loads(request.data)

  # We get the purchase from the database
  purchase = Purchase.query.filter_by(id=idx).first()

  # We check if the purchase exists
  if purchase is None:
    return make_response('No existe compra.', 404)
  else:
    # We check if the fields are in the data
    if not (
      'date' in data
      and 'id_number' in data
      and 'name' in data
      and 'price' in data
      and 'qty' in data
      and 'humidity' in data
      and 'depletion' in data
      and 'total_qty' in data
      and 'amount' in data
      and 'description' in data
    ):
      return make_response('No hay suficiente informacion para crear el producto.', 400)
    
    # We find the product
    product = Product(
      date=data['date'],
      id_type=data['id_type'],
      id_number=data['id_number'],
      name=data['name'],
      price=data['price'],
      qty=data['qty'],
      humidity=data['humidity'],
      depletion=data['depletion'],
      total_qty=data['total_qty'],
      amount=data['amount'],
      description=data['description'],
      purchase_id=purchase.id
    )

    # We add the product to the purchase
    purchase.item_qty += int(data['qty'])
    purchase.total_price += float(data['price']) * int(data['qty'])
    db.session.add(product)

    # We commit the changes to the database
    db.session.commit()

    return make_response('Product added.', 201)

# Delete the product of the purchase
@harvests_bp.route(routes["harvests"]["purchases"] + '/<int:idx>/product/<int:product_idx>', endpoint="delete-product", methods=['DELETE'])
@authorize_required
def delete_product(idx, product_idx):
  # We get the purchase from the database
  purchase = Purchase.query.filter_by(id=idx).first()

  # We check if the purchase exists
  if purchase is None:
    return make_response('No existe compra.', 404)
  else:
    # We get the product from the database
    product = Product.query.filter_by(id=product_idx).first()

    # We check if the product exists
    if product is None:
      return make_response('No existe producto.', 404)
    else:
      # We delete the product
      db.session.delete(product)

      # We commit the changes to the database
      db.session.commit()

      return make_response('Product deleted.', 200)