from lecopain.dao.models import Subscription, Product, Customer
from lecopain.app import app, db
from lecopain.form import SubscriptionForm
from lecopain.services.subscription_manager import SubscriptionManager

from sqlalchemy import extract
from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, Flask, request, jsonify
from flask_login import login_required

app = Flask(__name__, instance_relative_config=True)

subscription_page = Blueprint('subscription_page', __name__,
                              template_folder='../templates')

subscriptionServices = SubscriptionManager()

#####################################################################
#                                                                   #
#####################################################################
@subscription_page.route("/subscriptions/customers/<int:customer_id>", methods=['GET', 'POST'])
@login_required
def subscriptions(customer_id):

    if customer_id == 0 or customer_id == None:
        subscriptions = Subscription.query.order_by(
            Subscription.start_date.desc()).all()
    else:
        subscriptions = Subscription.query.filter(
            Subscription.customer_id == customer_id).order_by(Subscription.start_date.desc()).all()

    customers = Customer.query.all()
    map = subscriptionServices.get_maps_from_subscriptions(subscriptions)

    return render_template('/subscriptions/subscriptions.html', subscriptions=subscriptions, customers=customers, title="Toutes les abonnements", map=map)


#####################################################################
#                                                                   #
#####################################################################
# """ @subscription_page.route("/subscriptions/new", methods=['GET', 'POST'])
# @login_required
# def subscription_create():
#     form = SubscriptionForm()
#     tmp_products = request.form.getlist('products')
#     tmp_quantities = request.form.getlist('quantities')
#     tmp_prices = request.form.getlist('prices')

#     if form.validate_on_submit():
#         subcription = Subscription(title=form.title.data, status=form.status.data, customer_id=int(
#             form.customer_id.data), shipping_dt=form.shipping_dt.data)
#         subscriptionServices.create_subscription(
#             subcription=subcription, tmp_products=tmp_products, tmp_quantities=tmp_quantities, tmp_prices=tmp_prices)
#         #flash(f'People created for {form.firstname.data}!', 'success')
#         redirect('/subscriptions/customers/0')
#     else:
#         customers = Customer.query.all()
#         products = Product.query.all()
#     # else:
#     #    flash(f'Failed!', 'danger')
#     subscriptionStatusList = _get_subscription_frequency()

#     return r """ender_template('/subscriptions/create_subscription.html', title='Creation d\'abonnement', form=form, customers=customers, products=products, subscriptionStatusList=subscriptionStatusList)
