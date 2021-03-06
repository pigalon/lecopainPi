from flask import (Flask, 
                   Blueprint, 
                   render_template, 
                   url_for,  
                   flash, 
                   redirect, 
                   jsonify, 
                   request, 
                   session,
                   send_from_directory)
from flask_login import login_required, current_user
from datetime import datetime
import locale
from lecopain.app import app, db
from lecopain.form import PersonForm, OrderForm, ProductForm, LoginForm
from lecopain.dao.models import Customer, Seller, Order, Product, Seller, User, Subscription, Shipment, Stat
import lecopain.dao.events_session

from lecopain.controllers.customer_controller import customer_page
from lecopain.controllers.shipment_controller import shipment_page
from lecopain.controllers.order_controller import order_page
from lecopain.controllers.product_controller import product_page
from lecopain.controllers.seller_controller import seller_page
from lecopain.controllers.user_controller import user_page
from lecopain.controllers.subscription_controller import subscription_page
from lecopain.controllers.report_controller import report_page

from lecopain.controllers.customer.report_controller       import customer_report_page
from lecopain.controllers.customer.subscription_controller import customer_subscription_page
from lecopain.controllers.customer.shipment_controller     import customer_shipment_page
from lecopain.controllers.customer.main_controller         import customer_main_page

from lecopain.controllers.seller.report_controller          import seller_report_page
from lecopain.controllers.seller.product_controller         import seller_product_page
from lecopain.controllers.seller.main_controller            import seller_main_page

from lecopain.services.user_manager                         import UserManager
from lecopain.services.shipment_manager                     import ShipmentManager
from lecopain.services.subscription_manager                 import SubscriptionManager
from lecopain.services.customer_manager                     import CustomerManager
from lecopain.services.seller_manager                       import SellerManager
from lecopain.services.product_manager                      import ProductManager
from lecopain.services.order_manager                        import OrderManager


from flasgger import Swagger
from flasgger.utils import swag_from

userServices         = UserManager()
shipmentServices     = ShipmentManager()
subscriptionServices = SubscriptionManager()
customerServices     = CustomerManager()
sellerServices       = SellerManager()
productServices      = ProductManager()
orderServices        = OrderManager()

app.register_blueprint(seller_page)
app.register_blueprint(customer_page)
app.register_blueprint(shipment_page)
app.register_blueprint(order_page)
app.register_blueprint(product_page)
app.register_blueprint(seller_page)
app.register_blueprint(user_page)
app.register_blueprint(subscription_page)
app.register_blueprint(report_page)

app.register_blueprint(customer_main_page)
app.register_blueprint(customer_shipment_page)
app.register_blueprint(customer_subscription_page)
app.register_blueprint(customer_report_page)

app.register_blueprint(seller_main_page)
app.register_blueprint(seller_product_page)
app.register_blueprint(seller_report_page)

seller_page = Blueprint('seller_page',  __name__,
                        template_folder='./templates')
customer_page = Blueprint('customer_page',  __name__,
                        template_folder='./templates')
shipment_page = Blueprint('shipment_page',  __name__,
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

customer_main_page = Blueprint('customer_main_page',  __name__,
                        template_folder='./templates')
customer_shipment_page = Blueprint('customer_shipment_page',  __name__,
                        template_folder='./templates')
customer_subscription_page = Blueprint('customer_subscription_page',  __name__,
                        template_folder='./templates')
customer_subscription_page = Blueprint('customer_report_page',  __name__,
                        template_folder='./templates')

seller_main_page = Blueprint('seller_main_page',  __name__,
                        template_folder='./templates')
seller_shipment_page = Blueprint('seller_order_page',  __name__,
                        template_folder='./templates')
seller_subscription_page = Blueprint('seller_products_page',  __name__,
                        template_folder='./templates')
seller_subscription_page = Blueprint('seller_report_page',  __name__,
                        template_folder='./templates')

Swagger(app)

@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
@swag_from('specs/home.yml')
def home():
    if current_user.is_authenticated and current_user.is_active:
        app.logger.info("User connected : " + str(current_user) +
                            " with IP address : " + str(request.remote_addr))
        
        
        user_id = current_user.get_id()
        user = userServices.get_by_username(user_id)
        if user.get_main_role() == 'customer_role':
            customer = customerServices.get_one(current_user.account_id)
            shipments_nb = shipmentServices.count_by_customer(customer_id=customer.id)
            subscriptions_nb = subscriptionServices.count_by_customer(customer_id=customer.id)
            return render_template('/customer/base.html', subscriptions_nb=subscriptions_nb, shipments_nb=shipments_nb, customer_id=user.account_id)
        if user.get_main_role() == 'seller_role':
            seller = sellerServices.get_one(current_user.account_id)
            products_nb = productServices.count_by_seller(seller_id=seller.id)
            orders_nb = orderServices.count_by_seller(seller_id=seller.id)
            return render_template('/seller/base.html', products_nb=products_nb, orders_nb=orders_nb, seller_id=user.account_id)
        if user.get_main_role() == 'admin_role':
            customers_nb = Customer.query.count()
            orders_nb = Order.query.count()
            products_nb = Product.query.count()
            sellers_nb = Seller.query.count()
            subscriptions_nb = Subscription.query.count()
            shipments_nb = Shipment.query.count()
            stat = Stat.query.get_or_404(1)
            return render_template('base.html', customers_nb=customers_nb, orders_nb=orders_nb, products_nb=products_nb, sellers_nb=sellers_nb, subscriptions_nb=subscriptions_nb, shipments_nb=shipments_nb, stat=stat)
    else:
        app.logger.info("Need to be authenticated: " +
                        " with IP address : " + str(request.remote_addr))
        return redirect(url_for('user_page.login'))
    
    @app.route('/favicon.ico')
    def favicon():
        return send_from_directory(os.path.join(app.root_path, 'static'),
                                'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
