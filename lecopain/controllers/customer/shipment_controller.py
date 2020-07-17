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

from lecopain.helpers.roles_utils import customer_login_required

app = Flask(__name__, instance_relative_config=True)

customer_shipment_page = Blueprint('customer_shipment_page', __name__,
                       template_folder='../templates')

shipmentServices = ShipmentManager()
customerService = CustomerManager()
productService = ProductManager()



#####################################################################
#                                                                   #
#####################################################################
@customer_shipment_page.route("/shipments", methods=['GET', 'POST'])
@login_required
@customer_login_required
def shipments():
    return render_template('/shipments/shipments.html', title="Livraisons")



#####################################################################
#                                                                   #
#####################################################################
@customer_shipment_page.route("/shipments/<int:shipment_id>", methods=['GET', 'POST'])
@login_required
@customer_login_required
def shipment(shipment_id):
    shipment = shipmentServices.get_one(shipment_id)
    return render_template('/shipments/shipment.html', shipment=shipment)




#####################################################################
#                                                                   #
#####################################################################
@customer_shipment_page.route('/api/shipments/subscriptions/<int:subscription_id>')
@login_required
@customer_login_required
def api_shipments_by_subscription(subscription_id):
    
    page = request.args.get("page")
    per_page = request.args.get("per_page")

    if page is None:
        page = 1
    if per_page is None:
        per_page=10
        
    data, prev_page, next_page = shipmentServices.get_all_by_subscription_pagination(subscription_id, page=int(page), per_page=int(per_page))
    
    return jsonify(Pagination.get_paginated_db(
        data, '/api/shipments/subscriptions/'+str(subscription_id),
        page=request.args.get('page', page),
        per_page=request.args.get('per_page', per_page),
        prev_page=prev_page, next_page=next_page ))


#####################################################################
#                                                                   #
#####################################################################
@customer_shipment_page.route('/api/shipments/period/<string:period>/date/<string:day>')
@login_required
@customer_login_required
def api_day_shipments(period, day):
    page = request.args.get("page")
    per_page = request.args.get("per_page")

    if page is None:
        page = 1
    if per_page is None:
        per_page=10
    
    data, prev_page, next_page = shipmentServices.get_some_pagination(period=period, day=day, customer_id=customer_id, page=int(page), per_page=int(per_page))

    return jsonify(Pagination.get_paginated_db(
        data, '/api/shipments/period/'+period+'/date/'+day+'/customers/'+str(customer_id),
        page=request.args.get('page', page),
        per_page=request.args.get('per_page', per_page),
        prev_page=prev_page, next_page=next_page))