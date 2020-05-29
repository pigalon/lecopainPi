from lecopain.dao.models import Product, Seller, ProductStatus
from lecopain.app import app, db
from lecopain.form import ProductForm
from flask import session, Blueprint, render_template, redirect, url_for, Flask, jsonify
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
                   'price': form.price.data,
                   'seller_id': form.seller_id.data,
                   'description': form.description.data,
                   'category': form.category.data
                 }
        product = productServices.create(product)
        return redirect(url_for('product_page.products'))
    return render_template('/products/create_product.html', title='Product form', form=form, sellers=sellers)

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

    return render_template('/products/update_product.html', product=product, title='Mise a jour de produit', form=form, sellers=sellers)

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
    return render_template('/products/delete_product.html', product=product, title='Suppression de produit')

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
    return jsonify({'products': productServices.get_all_by_seller(seller_id)})
