from flask import Flask, Blueprint, render_template, url_for,  flash, redirect, jsonify, request
from datetime import datetime
import locale
from lecopain import app, db
from lecopain.form import PersonForm, OrderForm, ProductForm
from lecopain.dao.models import Customer, CustomerOrder, Product, Vendor

from lecopain.controllers.customer_controller import customer_page
from lecopain.controllers.order_controller import order_page
from lecopain.controllers.product_controller import product_page
from lecopain.controllers.vendor_controller import vendor_page
from lecopain.controllers.delivery_controller import delivery_page


app.register_blueprint(customer_page)
app.register_blueprint(order_page)
app.register_blueprint(product_page)
app.register_blueprint(vendor_page)
app.register_blueprint(delivery_page)



customer_page                                      = Blueprint('customer_page',  __name__,
                        template_folder            = './templates')
order_page                                         = Blueprint('order_page',  __name__,
                        template_folder            = './templates')
product_page                                       = Blueprint('product_page',  __name__,
                        template_folder            = './templates')
vendor_page                                        = Blueprint('vendor_page',  __name__,
                        template_folder            = './templates')
delivery_page                                      = Blueprint('delivery_page',  __name__,
                        template_folder            = './templates')


#app                                               = Flask(__name__,instance_relative_config = True)

locale.setlocale(locale.LC_TIME, "fr_FR")


@app.route("/")
@app.route("/home")
def index()                                        : 
    customers_nb = Customer.query.count()
    orders_nb = CustomerOrder.query.count()
    products_nb = Product.query.count()
    vendors_nb = Vendor.query.count()
    
    return render_template('base.html', customers_nb=customers_nb, orders_nb=orders_nb, products_nb=products_nb, vendors_nb=vendors_nb)

@app.route("/home2")
def home()                                         : 
    return render_template('home.html')

@app.route('/_get_customers/')
def _get_customers()                               : 
    customers                                      = [(row.id, row.firstname) for row in Customer.query.all()]
    return jsonify(customers)


if __name__ == '__main__': 
     app.run(host                                  = '0.0.0.0', port                         = 5000)


