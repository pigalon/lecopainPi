from lecopain.dao.models import Subscription, Product, Customer
from lecopain.app import app, db
from lecopain.form import SubscriptionForm
from lecopain.services.subscription_manager import SubscriptionManager
from lecopain.services.customer_manager import CustomerManager
from lecopain.services.seller_manager import SellerManager


from sqlalchemy import extract
from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, Flask, request, jsonify
from flask_login import login_required

app = Flask(__name__, instance_relative_config=True)

subscription_page = Blueprint('subscription_page', __name__,
                              template_folder='../templates')

subscriptionServices = SubscriptionManager()
customerServices = CustomerManager()
sellerServices = SellerManager()


#####################################################################
#                                                                   #
#####################################################################
@subscription_page.route("/subscriptions", methods=['GET', 'POST'])
@login_required
def subscriptions():
    return render_template('/subscriptions/subscriptions.html', title="Abonnements")

#####################################################################
#                                                                   #
#####################################################################
@subscription_page.route("/subscriptions/<int:subscription_id>", methods=['GET', 'POST'])
@login_required
def subscription(subscription_id):
    subscription = subscriptionServices.get_one(subscription_id)
    return render_template('/subscriptions/subscription.html', subscription=subscription)

#####################################################################
#                                                                   #
#####################################################################
@subscription_page.route('/api/subscriptions/')
@login_required
def api_subscriptions():
    return jsonify({'subscriptions': subscriptionServices.get_all()})

#####################################################################
#                                                                   #
#####################################################################
@subscription_page.route('/api/subscriptions/period/<string:period>/customers/<int:customer_id>')
@login_required
def api_day_subscriptions(period, customer_id):
    return jsonify({'subscriptions': subscriptionServices.get_some(period=period, customer_id=customer_id)})

#####################################################################
#                                                                   #
#####################################################################
@subscription_page.route("/subscriptions/new", methods=['GET', 'POST'])
@login_required
def subscription_create():
    form = SubscriptionForm()

    subscription = {
            'customer_id': form.customer_id.data,
            'seller_id': form.seller_id.data,
            'start_dt': form.start_dt.data,
            'end_dt': form.end_dt.data,
            }

    if form.validate_on_submit():
        subscriptionServices.create_subscription(
            subscription=subscription)
        return redirect('/subscriptions')

    sellers = sellerServices.optim_get_all()
    customers = customerServices.optim_get_all()

    return render_template('/subscriptions/create_subscription.html', title='Creation de commande', form=form, customers=customers, sellers=sellers)

#####################################################################
#                                                                   #
#####################################################################
@subscription_page.route("/subscriptions/delete/<int:subscription_id>")
@login_required
def display_delete_subscription(subscription_id):
    subscription = subscriptionServices.get_one(subscription_id)
    return render_template('/subscriptions/delete_subscription.html', subscription=subscription, title='Suppression de commande')

#####################################################################
#                                                                   #
#####################################################################
@subscription_page.route("/subscriptions/<int:subscription_id>", methods=['DELETE'])
@login_required
def delete_subscription(subscription_id):
    subscriptionServices.delete_subscription(subscription_id)
    return jsonify({})

#####################################################################
#                                                                   #
#####################################################################
@subscription_page.route("/subscriptions/days/<int:subscription_day_id>", methods=['GET', 'POST'])
@login_required
def subscription_day(subscription_day_id):
    subscription_day = subscriptionServices.get_one_day(subscription_day_id)
    return render_template('/subscriptions/subscription_day.html', subscription_day=subscription_day)
