from lecopain.dao.models import ShipmentStatus_Enum,  ShippingStatus_Enum, PaymentStatus_Enum
from lecopain.app import app
from lecopain.form import ShipmentForm, ShippingDtForm, CancellationForm
from lecopain.services.shipment_manager import ShipmentManager, Period_Enum
from lecopain.services.customer_manager import CustomerManager
from lecopain.services.product_manager import ProductManager
from lecopain.helpers.pagination import Pagination

from sqlalchemy import extract
from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, Flask, request, jsonify
from flask_login import login_required

from lecopain.helpers.roles_utils import admin_login_required
import json

app = Flask(__name__, instance_relative_config=True)

shipment_page = Blueprint('shipment_page', __name__,
                       template_folder='../templates')

shipmentServices = ShipmentManager()
customerService = CustomerManager()
productService = ProductManager()



#####################################################################
#                                                                   #
#####################################################################
@shipment_page.route("/shipments", methods=['GET', 'POST'])
@login_required
@admin_login_required
def shipments():
    return render_template('/shipments/shipments.html', title="Livraisons")

#####################################################################
#                                                                   #
#####################################################################
@shipment_page.route("/shipments/new", methods=['GET', 'POST'])
@login_required
@admin_login_required
def shipment_create():
    form = ShipmentForm()

    lines = (
        request.form.getlist('product_id[]'),
        request.form.getlist('seller_id[]'),
        request.form.getlist('quantity[]'),
        request.form.getlist('price[]'),
    )

    shipment = {'title': form.title.data,
            'customer_id': form.customer_id.data,
            'shipping_dt': form.shipping_dt.data,
            'category': form.category_name.data,
            'subscription_id': form.subscription_id.data,
    }
    

    if form.validate_on_submit():
        shipmentServices.create_shipment_and_parse_line(
            shipment=shipment, lines=lines)
        #flash(f'People created for {form.firstname.data}!', 'success')
        return redirect('/shipments')

    customers = customerService.optim_get_all()
    subscription_id = request.args.get("subscription_id")

    return render_template('/shipments/create_shipment.html', title='Creation de livraison', form=form, customers=customers, subscription_id=subscription_id)


#####################################################################
#                                                                   #
#####################################################################
@shipment_page.route("/shipments/update/<int:shipment_id>", methods=['GET', 'POST'])
@login_required
@admin_login_required
def shipment_update(shipment_id):
    form = ShipmentForm()
    
    category = form.category_name.data
    lines = (
        request.form.getlist('product_id[]'),
        request.form.getlist('seller_id[]'),
        request.form.getlist('quantity[]'),
        request.form.getlist('price[]'),
    )

    if form.validate_on_submit():
        shipmentServices.update_shipment_and_parse_line(category=category,
            shipment_id=shipment_id, lines=lines)
        #flash(f'People created for {form.firstname.data}!', 'success')
        return redirect(f'/shipments')

    shipment = shipmentServices.get_one(shipment_id)
    str_lines = ''
    for order in shipment['orders']:
        if str_lines == '':
            str_lines = str(order['lines']).replace("[", "").replace("]", "")
        else:
            str_lines = str_lines + "," + str(order['lines']).replace("[", "").replace("]", "")
    str_lines = "[" + str_lines.replace("{", "\{").replace("}", "\}") + "]"

    return render_template('/shipments/update_shipment.html', shipment=shipment, str_lines=str_lines, title='Mise à jour de livraison', form=form)


#####################################################################
#                                                                   #
#####################################################################
@shipment_page.route("/shipments/<int:shipment_id>", methods=['GET', 'POST'])
@login_required
@admin_login_required
def shipment(shipment_id):
    shipment = shipmentServices.get_one(shipment_id)
    return render_template('/shipments/shipment.html', shipment=shipment)

#####################################################################
#                                                                   #
#####################################################################
@shipment_page.route("/shipments/<int:shipment_id>/shipping_dt", methods=['GET', 'POST'])
@login_required
@admin_login_required
def display_update_shipment_time(shipment_id):

    shipment = shipmentServices.get_one(shipment_id)
    form = ShippingDtForm()

    if form.validate_on_submit():
        shipmentServices.update_shipping_dt(
            shipment, shipping_dt=form.shipping_dt.data)
        return redirect(f'/shipments')

    return render_template('/shipments/update_shipping_dt.html', shipment=shipment, title='Mise a jour du jour de la livraison', form=form)

#####################################################################
#                                                                   #
#####################################################################
@shipment_page.route("/shipments/<int:shipment_id>/cancel", methods=['GET', 'POST'])
@login_required
@admin_login_required
def display_update_shipment_annulation(shipment_id):
    shipmentServices.update_shipment_status(shipment_id, ShipmentStatus_Enum.ANNULEE.value)
    return redirect(f'/shipments/{shipment_id}')

#####################################################################
#                                                                   #
#####################################################################

@shipment_page.route("/shipments/<int:shipment_id>/created", methods=['GET', 'POST'])
@login_required
@admin_login_required
def display_update_shipment_created(shipment_id):
    shipmentServices.update_shipment_status(shipment_id, ShipmentStatus_Enum.CREE.value)
    return redirect(f'/shipments/{shipment_id}')

#####################################################################
#                                                                   #
#####################################################################

@shipment_page.route("/shipments/<int:shipment_id>/shipped/<string:status>", methods=['GET', 'POST'])
@login_required
@admin_login_required
def update_shipment_shipped(shipment_id, status):
    if status == 'NON':
        shipmentServices.update_shipment_shipping_status(shipment_id, ShippingStatus_Enum.NON.value)
    else:
        shipmentServices.update_shipment_shipping_status(shipment_id, ShippingStatus_Enum.OUI.value)
    return redirect('/shipments')

#####################################################################
#                                                                   #
#####################################################################


@shipment_page.route("/shipments/<int:shipment_id>/paid/<string:status>", methods=['GET', 'POST'])
@login_required
@admin_login_required
def update_shipment_paid(shipment_id, status):
    if status == 'NON':
        shipmentServices.update_shipment_payment_status(
            shipment_id, PaymentStatus_Enum.NON.value)
    else:
        shipmentServices.update_shipment_payment_status(
            shipment_id, PaymentStatus_Enum.OUI.value)
    return redirect('/shipments')


#####################################################################
#                                                                   #
#####################################################################
@shipment_page.route("/shipments/delete/<int:shipment_id>")
@login_required
@admin_login_required
def display_delete_shipment(shipment_id):
    shipment = shipmentServices.get_one(shipment_id)
    return render_template('/shipments/delete_shipment.html', shipment=shipment, title='Suppression de livraison')

#####################################################################
#                                                                   #
#####################################################################
@shipment_page.route("/shipments/<int:shipment_id>", methods=['DELETE'])
@login_required
@admin_login_required
def delete_shipment(shipment_id):
    shipmentServices.delete_shipment(shipment_id)
    return jsonify(success=True)

#####################################################################
#                                                                   #
#####################################################################
@shipment_page.route('/api/shipments/')
@login_required
@admin_login_required
def api_shipments():
    return jsonify({'shipments': shipmentServices.get_all()})

#####################################################################
#                                                                   #
#####################################################################
@shipment_page.route('/api/shipments/pay/', methods=['POST'])
@login_required
@admin_login_required
def pai_pay_list():
  data = json.loads(request.data)
  for item in data :
    if item['id'] != '':
      shipmentServices.update_shipment_payment_status(item['id'], PaymentStatus_Enum.OUI.value)
  return jsonify({'shipments': ''})

#####################################################################
#                                                                   #
#####################################################################
@shipment_page.route('/api/shipments/cancel/', methods=['POST'])
@login_required
@admin_login_required
def pai_cancel_list():
  data = json.loads(request.data)
  for item in data :
    if item['id'] != '':
      shipmentServices.update_shipment_status(item['id'], ShipmentStatus_Enum.ANNULEE.value)
  return jsonify({'shipments': ''})

#####################################################################
#                                                                   #
#####################################################################
@shipment_page.route('/api/shipments/undo/', methods=['POST'])
@login_required
@admin_login_required
def pai_undo_list():
  data = json.loads(request.data)
  for item in data :
    if item['id'] != '':
      shipmentServices.update_shipment_status(item['id'], ShipmentStatus_Enum.CREE.value)
  return jsonify({'shipments': ''})

#####################################################################
#                                                                   #
#####################################################################
@shipment_page.route('/api/shipments/subscriptions/<int:subscription_id>')
@login_required
@admin_login_required
def api_shipments_by_subscription(subscription_id):
   return jsonify({'shipments': shipmentServices.get_all_by_subscription(subscription_id, nocanceled=False, nopaid=False)})

    
    #return jsonify({'shipments': shipmentServices.get_all_by_subscription(subscription_id)})

#####################################################################
#                                                                   #
#####################################################################
@shipment_page.route('/api/shipments/customers/<int:customer_id>')
@login_required
@admin_login_required
def api_shipments_by_customer(customer_id):
    page = request.args.get("page")
    per_page = request.args.get("per_page")

    if page is None:
        page = 1
    if per_page is None:
        per_page=10
    
    data, prev_page, next_page = shipmentServices.get_all_by_customer_pagination(customer_id, page=int(page), per_page=int(per_page))
    
    return jsonify(Pagination.get_paginated_db(
        data, '/api/shipments/customers/'+str(customer_id),
        page=request.args.get('page', page),
        per_page=request.args.get('per_page', per_page),
        prev_page=prev_page, next_page=next_page ))
    #return jsonify({'shipments': shipmentServices.get_all_by_customer(customer_id)})

#####################################################################
#                                                                   #
#####################################################################
@shipment_page.route('/api/shipments/sellers/<int:seller_id>')
@login_required
@admin_login_required
def api_shipments_by_seller(seller_id):
    return jsonify({'shipments': shipmentServices.get_all_by_seller(seller_id)})


#####################################################################
#                                                                   #
#####################################################################
@shipment_page.route('/api/shipments/period/<string:period>/date/<string:day>/customers/<int:customer_id>')
@login_required
@admin_login_required
def api_day_shipments(period, day, customer_id):
    page = request.args.get("page")
    per_page = request.args.get("per_page")

    if page is None:
        page = 1
    if per_page is None:
        per_page=30
    
    data, prev_page, next_page = shipmentServices.get_some_pagination(period=period, day=day, customer_id=customer_id, page=int(page), per_page=int(per_page), nocanceled=False)

    return jsonify(Pagination.get_paginated_db(
        data, '/api/shipments/period/'+period+'/date/'+day+'/customers/'+str(customer_id),
        page=request.args.get('page', page),
        per_page=request.args.get('per_page', per_page),
        prev_page=prev_page, next_page=next_page))

#####################################################################
#                                                                   #
#####################################################################
@shipment_page.route('/api/shipments/period/<string:period>/date/<string:day>/customers/<int:customer_id>/nocanceled')
@login_required
@admin_login_required
def api_day_shipments_no_canceled(period, day, customer_id):
    page = request.args.get("page")
    per_page = request.args.get("per_page")

    if page is None:
        page = 1
    if per_page is None:
        per_page=30
    
    data, prev_page, next_page = shipmentServices.get_some_pagination(
        period=period, day=day, customer_id=customer_id, page=int(page), per_page=int(per_page), nocanceled=True, nopaid=False)

    return jsonify(Pagination.get_paginated_db(
        data, '/api/shipments/period/'+period+'/date/'+day+'/customers/'+str(customer_id)+'/nocanceled',
        page=request.args.get('page', page),
        per_page=request.args.get('per_page', per_page),
        prev_page=prev_page, next_page=next_page))


#####################################################################
#                                                                   #
#####################################################################
@shipment_page.route('/api/shipments/period/<string:period>/date/<string:day>/customers/<int:customer_id>/nopaid')
@login_required
@admin_login_required
def api_day_shipments_no_paid(period, day, customer_id):
    page = request.args.get("page")
    per_page = request.args.get("per_page")

    if page is None:
        page = 1
    if per_page is None:
        per_page=30
    
    data, prev_page, next_page = shipmentServices.get_some_pagination(
        period=period, day=day, customer_id=customer_id, page=int(page), per_page=int(per_page), nocanceled=False, nopaid=True)

    return jsonify(Pagination.get_paginated_db(
        data, '/api/shipments/period/'+period+'/date/'+day+'/customers/'+str(customer_id)+'/paid',
        page=request.args.get('page', page),
        per_page=request.args.get('per_page', per_page),
        prev_page=prev_page, next_page=next_page))

#####################################################################
#                                                                   #
#####################################################################
@shipment_page.route('/api/shipments/period/<string:period>/date/<string:day>/customers/<int:customer_id>/nocanceled/nopaid')
@login_required
@admin_login_required
def api_day_shipments_no_canceled_no_paid(period, day, customer_id):
    page = request.args.get("page")
    per_page = request.args.get("per_page")

    if page is None:
        page = 1
    if per_page is None:
        per_page=30
    
    data, prev_page, next_page = shipmentServices.get_some_pagination(
        period=period, day=day, customer_id=customer_id, page=int(page), per_page=int(per_page), nocanceled=True, nopaid=True)

    return jsonify(Pagination.get_paginated_db(
        data, '/api/shipments/period/'+period+'/date/'+day+'/customers/'+str(customer_id)+'/nocanceled/nopaid',
        page=request.args.get('page', page),
        per_page=request.args.get('per_page', per_page),
        prev_page=prev_page, next_page=next_page))

#####################################################################
#                                                                   #
#####################################################################
@shipment_page.route('/api/shipments/subscriptions/<int:subscription_id>/nocanceled')
@login_required
@admin_login_required
def api_shipments_by_subscription_no_canceled(subscription_id):
    
    return jsonify({'shipments': shipmentServices.get_all_by_subscription(subscription_id, nocanceled=True, nopaid=False)})


#####################################################################
#                                                                   #
#####################################################################
@shipment_page.route('/api/shipments/subscriptions/<int:subscription_id>/nopaid')
@login_required
@admin_login_required
def api_shipments_by_subscription_no_paid(subscription_id):
    
  return jsonify({'shipments': shipmentServices.get_all_by_subscription(subscription_id, nocanceled=False, nopaid=True)})

#####################################################################
#                                                                   #
#####################################################################
@shipment_page.route('/api/shipments/subscriptions/<int:subscription_id>/nocanceled/nopaid')
@login_required
@admin_login_required
def api_shipments_by_subscription_no_canceled_paid(subscription_id):
    
  return jsonify({'shipments': shipmentServices.get_all_by_subscription(subscription_id, nocanceled=True, nopaid=True)})