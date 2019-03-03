from lecopain.models import Product
from lecopain import app, db
from lecopain.form import ProductForm
from flask import Blueprint, render_template, redirect, url_for, Flask

app = Flask(__name__, instance_relative_config=True)


product_page = Blueprint('product_page', __name__,
                        template_folder='../templates')
@product_page.route("/products", methods=['GET', 'POST'])
def products():
    products = Product.query.order_by(Product.name.desc()).all()

    return render_template('/products/products.html', products=products, title="Toutes les produits")

@product_page.route("/products/new", methods=['GET', 'POST'])
def product_create():
    form = ProductForm()
    print("product form : " + str(form.validate_on_submit()))
    if form.validate_on_submit():
        product = Product(name=form.name.data,  price=form.price.data, description=form.description.data)
        db.session.add(product)
        db.session.commit()
        #flash(f'People created for {form.firstname.data}!', 'success')
        return redirect(url_for('index'))
    return render_template('/products/create_product.html', title='Product form', form=form)
