from lecopain.dao.models import Product, Seller, ProductStatus
from lecopain.app import app, db
from lecopain.form import ProductForm
from lecopain.helpers.pagination import Pagination
from flask import session, Blueprint, render_template, redirect, request, url_for, Flask, jsonify
from flask_login import login_required, current_user
from sqlalchemy.orm import load_only
from lecopain.services.product_manager import ProductManager
from lecopain.services.seller_manager import SellerManager
from lecopain.services.user_manager import UserManager
from lecopain.dao.models import Category_Enum

from lecopain.helpers.roles_utils import seller_login_required

app = Flask(__name__, instance_relative_config=True)


seller_product_page = Blueprint('seller_product_page', __name__,
                        template_folder='../templates')

productServices = ProductManager()
sellerServices = SellerManager()
userService = UserManager()

#####################################################################
#                                                                   #
#####################################################################
@seller_product_page.route("/seller/products/<int:product_id>")
@login_required
@seller_login_required
def product(product_id):
    
    product = Product.query.get_or_404(product_id)
    seller = Seller.query.get_or_404(product.seller_id)
    return render_template('/seller/products/product.html', product=product, seller=seller)
#####################################################################
#                                                                   #
#####################################################################
@seller_product_page.route("/seller/products", methods=['GET', 'POST'])
@login_required
@seller_login_required
def products():
    user_id = current_user.get_id()
    user = userService.get_by_username(user_id)
    products = Product.query.order_by(Product.name.desc()).all()
    return render_template('/seller/products/products.html', 
    products=products, title="Tous les produits", seller_id=user.account_id)


#####################################################################
#                                                                   #
#####################################################################
@seller_product_page.route('/seller/api/products/')
@login_required
@seller_login_required
def api_products_by_seller():
    page = request.args.get("page")
    per_page = request.args.get("per_page")

    user_id = current_user.get_id()
    user = userService.get_by_username(user_id)
    seller_id=user.account_id

    if page is None:
        page = 1
    if per_page is None:
        per_page=10
        
    data, prev_page, next_page = productServices.get_all_by_seller_pagination(seller_id=seller_id, page=int(page), per_page=int(per_page))

    return jsonify(Pagination.get_paginated_db(
        data, '/seller/api/products/sellers/'+str(seller_id),
        page=request.args.get('page', page),
        per_page=request.args.get('per_page', per_page),
        prev_page=prev_page, next_page=next_page))

    #user_id = current_user.get_id()
