from lecopain.dao.models import OrderStatus_Enum,  ShippingStatus_Enum, PaymentStatus_Enum
from lecopain.app import app
from lecopain.form import OrderForm, ShippingDtForm, CancellationForm
from lecopain.services.order_manager import OrderManager, Period_Enum
from lecopain.services.seller_manager import SellerManager
from lecopain.services.product_manager import ProductManager
from lecopain.services.user_manager import UserManager

from lecopain.helpers.pagination import Pagination

from sqlalchemy import extract
from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, Flask, request, jsonify
from flask_login import login_required, current_user

from lecopain.helpers.roles_utils import seller_login_required

app = Flask(__name__, instance_relative_config=True)

seller_order_page = Blueprint('seller_order_page', __name__,
                       template_folder='../templates')

orderServices = OrderManager()
sellerService = SellerManager()
productService = ProductManager()
userService = UserManager()

#####################################################################
#                                                                   #
#####################################################################
@seller_order_page.route("/seller/orders", methods=['GET', 'POST'])
@login_required
@seller_login_required
def orders():
    return render_template('/seller/orders/orders.html', title="Commandes")

#####################################################################
#                                                                   #
#####################################################################
@seller_order_page.route('/seller/api/orders')
@login_required
@seller_login_required
def api_orders_by_seller():
    page = request.args.get("page")
    per_page = request.args.get("per_page")

    user_id = current_user.get_id()
    user = userService.get_by_username(user_id)
    seller_id=user.account_id
 
    if page is None:
        page = 1
    if per_page is None:
        per_page=10
        
    data, prev_page, next_page = orderServices.get_all_by_seller_pagination(seller_id, page=int(page), per_page=int(per_page))
    
    
    return jsonify(Pagination.get_paginated_db(
        data, '/api/orders/sellers/'+str(seller_id),
        page=request.args.get('page', page),
        per_page=request.args.get('per_page', per_page),
        prev_page=prev_page, next_page=next_page))

