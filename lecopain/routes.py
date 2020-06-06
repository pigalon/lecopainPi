from flask import Flask, Blueprint, render_template, url_for,  flash, redirect, jsonify, request, session
from flask_login import login_required, current_user
from datetime import datetime
import locale
from lecopain.app import app, db
from lecopain.form import PersonForm, OrderForm, ProductForm, LoginForm
from lecopain.dao.models import Customer, Order, Product, Seller, User, Subscription

from lecopain.controllers.customer_controller import customer_page
from lecopain.controllers.order_controller import order_page
from lecopain.controllers.product_controller import product_page
from lecopain.controllers.seller_controller import seller_page
from lecopain.controllers.user_controller import user_page
from lecopain.controllers.subscription_controller import subscription_page
from lecopain.controllers.report_controller import report_page


from werkzeug.security import generate_password_hash, check_password_hash

from flasgger import Swagger
from flasgger.utils import swag_from


app.register_blueprint(customer_page)
app.register_blueprint(order_page)
app.register_blueprint(product_page)
app.register_blueprint(seller_page)
app.register_blueprint(user_page)
app.register_blueprint(subscription_page)
app.register_blueprint(report_page)


customer_page = Blueprint('customer_page',  __name__,
                          template_folder='./templates')
order_page = Blueprint('order_page',  __name__,
                       template_folder='./templates')
product_page = Blueprint('product_page',  __name__,
                         template_folder='./templates')
seller_page = Blueprint('seller_page',  __name__,
                        template_folder='./templates')
user_page = Blueprint('user_page',  __name__,
                      template_folder='./templates')
subscription_page = Blueprint('subscription_page',  __name__,
                              template_folder='./templates')
report_page = Blueprint('report_page',  __name__,
                              template_folder='./templates')

Swagger(app)


#locale.setlocale(locale.LC_TIME, "fr_FR")


@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
@swag_from('specs/home.yml')
def home():
    if current_user.is_authenticated:
        customers_nb = Customer.query.count()
        orders_nb = Order.query.count()
        products_nb = Product.query.count()
        sellers_nb = Seller.query.count()
        subscriptions_nb = Subscription.query.count()
        return render_template('base.html', customers_nb=customers_nb, orders_nb=orders_nb, products_nb=products_nb, sellers_nb=sellers_nb)
    else:
        return redirect(url_for('user_page.login'))


@app.route("/home2", methods=['GET', 'POST'])
def home2():
    customers = [(row.id, row.firstname) for row in Customer.query.all()]
    return jsonify(customers)


@app.route('/_get_customers/')
def _get_customers():
    customers = [(row.id, row.firstname) for row in Customer.query.all()]
    return jsonify(customers)


@app.route("/settings")
@login_required
def settings():
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
