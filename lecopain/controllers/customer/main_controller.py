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
from flask_login import login_required, current_user

from lecopain.helpers.roles_utils import customer_login_required

app = Flask(__name__, instance_relative_config=True)

customer_main_page = Blueprint('customer_main_page', __name__,
                       template_folder='../templates')

shipmentServices = ShipmentManager()
customerService = CustomerManager()
productService = ProductManager()



#####################################################################
#                                                                   #
#####################################################################
@customer_main_page.route("/customer_home", methods=['GET', 'POST'])
@login_required
@customer_login_required
def home():
    
    customer = customerService.get_one(current_user.account_id)
    
    subscriptions_nb = 0#Subscription.query.count()
    shipments_nb = 0#Shipment.query.count()
        
    
        
    return render_template('/customer/base.html', subscriptions_nb=subscriptions_nb, shipments_nb=shipments_nb)


