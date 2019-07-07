from flask import Flask, Blueprint, render_template, url_for,  flash, redirect, jsonify, request, session
from flask_login import login_required
from datetime import datetime
import locale
from lecopain import app, db
from lecopain.form import PersonForm, OrderForm, ProductForm
from lecopain.dao.models import Customer, CustomerOrder, Product, Vendor, User

from lecopain.controllers.customer_controller import customer_page
from lecopain.controllers.order_controller import order_page
from lecopain.controllers.product_controller import product_page
from lecopain.controllers.vendor_controller import vendor_page
from lecopain.controllers.delivery_controller import delivery_page
from lecopain.controllers.user_controller import user_page

from werkzeug.security import generate_password_hash, check_password_hash


app.register_blueprint(customer_page)
app.register_blueprint(order_page)
app.register_blueprint(product_page)
app.register_blueprint(vendor_page)
app.register_blueprint(delivery_page)
app.register_blueprint(user_page)



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
user_page                                          = Blueprint('user_page',  __name__,
                        template_folder            = './templates')


#app                                               = Flask(__name__,instance_relative_config = True)

#locale.setlocale(locale.LC_TIME, "fr_FR")


@app.route("/")
@app.route("/home")
def home():
    print(generate_password_hash('melina30'))
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        customers_nb = Customer.query.count()
        orders_nb = CustomerOrder.query.count()
        products_nb = Product.query.count()
        vendors_nb = Vendor.query.count()

        user = User()
        for attr in dir(user):
            print("user.%s = %r" % (attr, getattr(user, attr)))
        
        return render_template('base.html', customers_nb=customers_nb, orders_nb=orders_nb, products_nb=products_nb, vendors_nb=vendors_nb)


#@app.route('/login', methods=['POST'])
#def do_admin_login():
#    if request.form['password'] == 'password' and request.form['username'] == 'admin':
#        session['logged_in'] = True
#    else:
#        flash('wrong password!')
#    return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route("/home2")
def home2()                                         : 
    return render_template('home.html')

@app.route('/_get_customers/')
def _get_customers()                               : 
    customers                                      = [(row.id, row.firstname) for row in Customer.query.all()]
    return jsonify(customers)


@app.login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

if __name__ == '__main__': 
     app.run(host                                  = '0.0.0.0', port                         = 5000)


