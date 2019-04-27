from lecopain.models import Product, Vendor, ProductStatus
from lecopain import app, db
from lecopain.form import ProductForm
from flask import session, Blueprint, render_template, redirect, url_for, Flask, jsonify
from sqlalchemy.orm import load_only

app = Flask(__name__, instance_relative_config=True)


product_page = Blueprint('product_page', __name__,
                        template_folder='../templates')

#####################################################################
#                                                                   #
#####################################################################
@product_page.route("/products/<int:product_id>")
def product(product_id):
    product = Product.query.get_or_404(product_id)
    vendor = Vendor.query.get_or_404(product.vendor_id)
    return render_template('/products/product.html', product=product, vendor=vendor)
#####################################################################
#                                                                   #
#####################################################################
@product_page.route("/products", methods=['GET', 'POST'])
def products():
    products = Product.query.order_by(Product.name.desc()).all()
    return render_template('/products/products.html', products=products, title="Toutes les produits")
#####################################################################
#                                                                   #
#####################################################################
@product_page.route("/products/new", methods=['GET', 'POST'])
def product_create():
    form = ProductForm()
    vendors = Vendor.query.all()
    print("product form : " + str(form.validate_on_submit()))
    if form.validate_on_submit():
        product = Product(name=form.name.data,  price=form.price.data, description=form.description.data)
        db.session.add(product)
        db.session.commit()
        #flash(f'People created for {form.firstname.data}!', 'success')
        return redirect(url_for('index'))
    productStatusList = _get_product_status()
    return render_template('/products/create_product.html', title='Product form', form=form, productStatusList=productStatusList, vendors=vendors)

#####################################################################
#                                                                   #
#####################################################################
@product_page.route("/products/update/<int:product_id>", methods=['GET', 'POST'])
def display_update_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm()

    vendors = Vendor.query.all()
    

    if form.validate_on_submit():
        print('update form validate : ' + str(product.id))

        #order_dt=datetime.strptime('YYYY-MM-DD HH:mm:ss', form.order_dt.data)
        productForm = Product(name=form.name.data, price=form.price.data, status=form.status.data, vendor_id=int(form.vendor_id.data), description=form.description.data)
        product.name = productForm.name
        product.status = productForm.status
        product.vendor_id = productForm.vendor_id
        product.description = productForm.description
        product.price = productForm.price

        db.session.commit()

       
        #flash(f'People created for {form.firstname.data}!', 'success')
        return redirect(url_for('product_page.products'))
    else:
        form.vendor_id.data = product.vendor_id
        form.description.data = product.description
        form.status.data = product.status
        form.name.data = product.name
        form.price.data = product.price
        

    productStatusList = _get_product_status()
    return render_template('/products/update_product.html', product=product, title='Mise a jour de produit', form=form, vendors=vendors,  productStatusList=productStatusList)

#####################################################################
#                                                                   #
#####################################################################
@product_page.route('/_get_product_status/')
def _get_product_status():
    productsStatusList = [(row.name) for row in ProductStatus.query.all()]
    return productsStatusList

#####################################################################
#                                                                   #
#####################################################################
@product_page.route("/products/delete/<int:product_id>")
def display_delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('/products/delete_product.html', product=product, title='Suppression de produit')

#####################################################################
#                                                                   #
#####################################################################
@product_page.route("/products/<int:product_id>", methods=['DELETE'])
def delete_order(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({})

#####################################################################
#                                                                   #
#####################################################################
@product_page.route("/_getjs_products/<int:vendor_id>")
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
