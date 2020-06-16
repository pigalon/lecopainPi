from lecopain.dao.models import Product, Seller, ProductStatus
from lecopain.app import app, db
from lecopain.form import ProductForm
from lecopain.helpers.pagination import Pagination
from flask import session, Blueprint, render_template, redirect, request, url_for, Flask, jsonify
from flask_login import login_required
from sqlalchemy.orm import load_only
from lecopain.services.product_manager import ProductManager
from lecopain.services.seller_manager import SellerManager

app = Flask(__name__, instance_relative_config=True)


product_page = Blueprint('product_page', __name__,
                         template_folder='../templates')

productServices = ProductManager()
sellerServices = SellerManager()

#####################################################################
#                                                                   #
#####################################################################
@product_page.route("/products/<int:product_id>")
@login_required
def product(product_id):
    product = Product.query.get_or_404(product_id)
    seller = Seller.query.get_or_404(product.seller_id)
    return render_template('/products/product.html', product=product, seller=seller)
#####################################################################
#                                                                   #
#####################################################################
@product_page.route("/products", methods=['GET', 'POST'])
@login_required
def products():
    products = Product.query.order_by(Product.name.desc()).all()
    return render_template('/products/products.html', products=products, title="Tous les produits")


#####################################################################
#                                                                   #
#####################################################################
@product_page.route("/products/new", methods=['GET', 'POST'])
@login_required
def product_create():
    form = ProductForm()
    
    sellers = sellerServices.optim_get_all()
    if form.validate_on_submit():
        product = {'name': form.name.data,
                   'short_name': form.short_name.data,
                   'price': form.price.data,
                   'seller_id': form.seller_id.data,
                   'description': form.description.data,
                   'category': form.category.data
                 }
        product = productServices.create(product)
        return redirect(url_for('product_page.products'))
    return render_template('/products/create_product.html', title='Ajouter un Produit', form=form, sellers=sellers)

#####################################################################
#                                                                   #
#####################################################################
@product_page.route("/products/update/<int:product_id>", methods=['GET', 'POST'])
@login_required
def display_update_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm()

    if form.validate_on_submit():
        print('update form validate : ' + str(product.id))

        productServices.update_product(form, product)

        #flash(f'People created for {form.firstname.data}!', 'success')
        return redirect(url_for('product_page.products'))

    productServices.convert_product_to_form(product=product, form=form)
    sellers = Seller.query.all()

    return render_template('/products/update_product.html', product=product, title='Mise a jour du produit', form=form, sellers=sellers)

#####################################################################
#                                                                   #
#####################################################################
@product_page.route('/_get_product_status/')
@login_required
def _get_product_status():
    productsStatusList = [(row.name) for row in ProductStatus.query.all()]
    return productsStatusList

#####################################################################
#                                                                   #
#####################################################################
@product_page.route("/products/delete/<int:product_id>")
@login_required
def display_delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('/products/delete_product.html', product=product, title='Suppression du produit')

#####################################################################
#                                                                   #
#####################################################################
@product_page.route("/products/<int:product_id>", methods=['DELETE'])
@login_required
def delete_order(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({})

#####################################################################
#                                                                   #
#####################################################################
@product_page.route('/api/products/sellers/<int:seller_id>')
@login_required
def api_products_by_seller(seller_id):
    data = productServices.get_all_by_seller(seller_id)
    start = request.args.get("start")
    limit = request.args.get("limit")
    if start is None:
        start = 1
    if limit is None:
        limit = 10

    return jsonify(Pagination.get_paginated_list(
        data, '/api/products/sellers/'+str(seller_id),
        start=request.args.get('start', int(start)),
        limit=request.args.get('limit', int(limit))))
    #return jsonify({'products': productServices.get_all_by_seller(seller_id)})

#####################################################################
#                                                                   #
#####################################################################
@product_page.route('/api/products/categories')
@login_required
def api_products_categories():
    return jsonify({'categories': productServices.get_all_categories()})

#####################################################################
#                                                                   #
#####################################################################
@product_page.route('/api/products/sellers/<int:seller_id>/categories/<string:category>')
@login_required
def api_products_by_seller_and_category(seller_id, category):
    return jsonify({'products': productServices.get_all_by_seller_category(seller_id, category)})
