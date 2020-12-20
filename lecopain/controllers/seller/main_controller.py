from lecopain.dao.models import ShipmentStatus_Enum,  ShippingStatus_Enum, PaymentStatus_Enum
from lecopain.app import app
from lecopain.form import ShipmentForm, ShippingDtForm, CancellationForm
from lecopain.services.report_manager import ReportManager
from lecopain.services.seller_manager import SellerManager
from lecopain.services.product_manager import ProductManager
from lecopain.services.order_manager import OrderManager
from lecopain.helpers.pagination import Pagination

from sqlalchemy import extract
from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, Flask, request, jsonify
from flask_login import login_required, current_user

from lecopain.helpers.roles_utils import seller_login_required

app = Flask(__name__, instance_relative_config=True)

seller_main_page = Blueprint('seller_main_page', __name__,
    template_folder='../templates')

reportService        = ReportManager()
sellerService        = SellerManager()
orderService         = OrderManager()
productService       = ProductManager()



#####################################################################
#                                                                   #
#####################################################################
@seller_main_page.route("/seller_home", methods=['GET', 'POST'])
@login_required
@seller_login_required
def home():
  seller = sellerService.get_one(current_user.account_id)
  orders_nb = orderService.count_by_seller(seller_id=seller.id)
  products_nb = productService.count_by_seller(seller_id=seller.id)
  return render_template('/seller/base.html', orders_nb=orders_nb, products_nb=products_nb, seller_id=seller.id)


