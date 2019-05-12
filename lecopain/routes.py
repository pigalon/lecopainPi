from flask import Flask, Blueprint, render_template, url_for,  flash, redirect, jsonify, request
from datetime import datetime
import locale
from lecopain import app, db
from lecopain.form import PersonForm, OrderForm, ProductForm
from lecopain.models import OrderStatus, Product, Order_product
from lecopain.dao.customer import Customer, CustomerOrder

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


customers2                                         = [
    {
        'id'                                       : 1,
        'firstname'                                : 'Jean',
        'lastname'                                 : 'Delatour',
        'email'                                    : 'jean.delatour@gmail.com',
        'address'                                  : '30 Rue Haute',
        'cp'                                       : '30413',
        'city'                                     : 'Langlade'
    },
    {
        'id'                                       : 2,
        'firstname'                                : 'Suzanne',
        'lastname'                                 : 'Vega',
        'email'                                    : 'suzanne.vega@gmail.com',
        'address'                                  : '58 Rue de Barcelone',
        'cp'                                       : '30000',
        'city'                                     : 'Nimes'
    }
]
locale.setlocale(locale.LC_TIME, "fr_FR")


@app.route("/")
@app.route("/home")
def index()                                        : 
    customers                                      = Customer.query.all()
    return render_template('index.html', customers = customers)

@app.route("/home2")
def home()                                         : 
    return render_template('home.html')

@app.route('/_get_customers/')
def _get_customers()                               : 
    customers                                      = [(row.id, row.firstname) for row in Customer.query.all()]
    return jsonify(customers)


if __name__ == '__main__': 
     app.run(host                                  = '0.0.0.0', port                         = 5000)


