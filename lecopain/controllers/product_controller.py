from lecopain.dao.models import Product, Vendor, ProductStatus
from lecopain import app, db
from lecopain.form import ProductForm
from flask import session, Blueprint, render_template, redirect, url_for, Flask, jsonify
from flask_login import login_required
from sqlalchemy.orm import load_only
from lecopain.services.product_manager import ProductManager

app = Flask(__name__, instance_relative_config=True)


product_page = Blueprint('product_page', __name__,
                        template_folder='../templates')

productManager = ProductManager()

#####################################################################
#                                                                   #
#####################################################################
@product_page.route("/products/<int:product_id>")
@login_required
def product(product_id):
    product = Product.query.get_or_404(product_id)
    vendor = Vendor.query.get_or_404(product.vendor_id)
    return render_template('/products/product.html', product=product, vendor=vendor)
#####################################################################
#                                                                   #
#####################################################################
@product_page.route("/products", methods=['GET', 'POST'])
@login_required
def products():
    products = Product.query.order_by(Product.name.desc()).all()
    return render_template('/products/products.html', products=products, title="Toutes les produits")
#####################################################################
#                                                                   #
#####################################################################
@product_page.route("/products/new", methods=['GET', 'POST'])
@login_required
def product_create():
    form = ProductForm()
    vendors = Vendor.query.all()
    print("product form : " + str(form.validate_on_submit()))
    if form.validate_on_submit():
        product = Product(name=form.name.data,  price=form.price.data, description=form.description.data)
        db.session.add(product)
        db.session.commit()
        #flash(f'People created for {form.firstname.data}!', 'success')
        return redirect(url_for('product_page.products'))
    productStatusList = _get_product_status()
    return render_template('/products/create_product.html', title='Product form', form=form, productStatusList=productStatusList, vendors=vendors)

#####################################################################
#                                                                   #
#####################################################################
@product_page.route("/products/update/<int:product_id>", methods=['GET', 'POST'])
@login_required
def display_update_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm()

    vendors = Vendor.query.all()
    

    if form.validate_on_submit():
        print('update form validate : ' + str(product.id))

        productManager.update_product(form, product)

        #flash(f'People created for {form.firstname.data}!', 'success')
        return redirect(url_for('product_page.products'))
    else:
        
        productManager.convert_product_to_form(product=product, form=form)

    productStatusList = _get_product_status()
    return render_template('/products/update_product.html', product=product, title='Mise a jour de produit', form=form, vendors=vendors,  productStatusList=productStatusList)

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
@product_page.route("/_getjs_products/<int:vendor_id>")
@login_required
def getjs_products(vendor_id):
    products = Product.query.filter(Product.vendor_id == vendor_id).options(load_only("name")).all()
    js_products = []
    data = {}
    data['id'] = " "
    data['name'] = " "
    js_products.append(data)


    for product in products :

        data = {}
        data['id'] = str(product.id)
        data['name'] = product.name

        js_products.append(data)

    return jsonify({'products': js_products})
