from lecopain.dao.models import Subscription, Product, Customer
from lecopain.app import app, db
from lecopain.form import SubscriptionForm, SubscriptionDayForm
from lecopain.services.subscription_manager import SubscriptionManager
from lecopain.services.customer_manager import CustomerManager
from lecopain.services.seller_manager import SellerManager
from lecopain.services.user_manager import UserManager
from lecopain.helpers.pagination import Pagination
from lecopain.helpers.date_utils import get_week_names


from sqlalchemy import extract
from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, Flask, request, jsonify
from flask_login import login_required, current_user

from lecopain.helpers.roles_utils import customer_login_required

app = Flask(__name__, instance_relative_config=True)

customer_subscription_page = Blueprint('customer_subscription_page', __name__,
                              template_folder='../templates')


subscriptionServices = SubscriptionManager()
customerServices = CustomerManager()
sellerServices = SellerManager()
userServices = UserManager()


#####################################################################
#                                                                   #
#####################################################################
@customer_subscription_page.route("/customer/subscriptions", methods=['GET', 'POST'])
@login_required
@customer_login_required
def subscriptions():
    user_id = current_user.get_id()
    user = userServices.get_by_username(user_id)
    return render_template('/customer/subscriptions/subscriptions.html', title="Abonnements", customer_id=user.account_id)

#####################################################################
#                                                                   #
#####################################################################
@customer_subscription_page.route("/customer/subscriptions/<int:subscription_id>", methods=['GET', 'POST'])
@login_required
@customer_login_required
def subscription(subscription_id):
    subscription = subscriptionServices.get_one(subscription_id)
    week_days = get_week_names()
    return render_template('/customer/subscriptions/subscription.html', subscription=subscription, week_days=week_days)

#####################################################################
#                                                                   #
#####################################################################
@customer_subscription_page.route('/api/customer/subscriptions/')
@login_required
@customer_login_required
def api_subscriptions():
    return jsonify({'subscriptions': subscriptionServices.get_all()})


#####################################################################
#                                                                   #
#####################################################################
@customer_subscription_page.route('/api/customer/subscriptions/period/<string:period>/date/<string:day>')
@login_required
@customer_login_required
def api_day_subscriptions(period, day):
    
    page = request.args.get("page")
    per_page = request.args.get("per_page")

    if page is None:
        page = 1
    if per_page is None:
        per_page=10
        
    user_id = current_user.get_id()
    user = userServices.get_by_username(user_id)
    
    data, prev_page, next_page = subscriptionServices.get_some_pagination(period=period, day=day, customer_id=user.account_id, page=int(page), per_page=int(per_page))
    
    return jsonify(Pagination.get_paginated_db(
        data, '/api/customer/subscriptions/period/'+period+'/date/'+day+'/customers/'+str(user.account_id),
        page=request.args.get('page', page),
        per_page=request.args.get('per_page', per_page),
        prev_page=prev_page, next_page=next_page))
    #return jsonify({'subscriptions': subscriptionServices.get_some(period=period, customer_id=customer_id)})



#####################################################################
#                                                                   #
#####################################################################
@customer_subscription_page.route("/customer/subscriptions/days/<int:subscription_day_id>", methods=['GET', 'POST'])
@login_required
@customer_login_required
def subscription_day(subscription_day_id):
    subscription_day = subscriptionServices.get_one_day(subscription_day_id)
    form = SubscriptionDayForm()

    lines = (
        request.form.getlist('product_id[]'),
        request.form.getlist('quantity[]'),
        request.form.getlist('price[]'),
    )

    if form.validate_on_submit():
        subscriptionServices.create_day_and_parse_line(
            subscription_day=subscription_day, lines=lines)
        return redirect('/customer/subscriptions/'+str(subscription_day.get('subscription')))

    return render_template('/customer/subscriptions/subscription_day.html', form=form, subscription_day=subscription_day)

#####################################################################
#                                                                   #
#####################################################################
@customer_subscription_page.route("/customer/subscriptions/<int:subscription_id>/weekdays/<int:week_day>", methods=['GET', 'POST'])
@login_required
@customer_login_required
def subscription_week_day(subscription_id, week_day):
    subscription_day = subscriptionServices.get_week_day(subscription_id, week_day)
    form = SubscriptionDayForm()
    

    if form.validate_on_submit():
        lines = (
            request.form.getlist('product_id[]'),
            request.form.getlist('seller_id[]'),
            request.form.getlist('quantity[]'),
            request.form.getlist('price[]'),
        )

        category =  form.category_name.data

        subscriptionServices.create_day_and_parse_line(
            subscription_day=subscription_day, lines=lines, category=category)
        return redirect('/customer/subscriptions/'+str(subscription_day.get('subscription')))

    return render_template('/customer/subscriptions/subscription_day.html', form=form, subscription_day=subscription_day)


#####################################################################
#                                                                   #
#####################################################################
@customer_subscription_page.route("/customer/subscriptions/days/<int:subscription_day_id>/cancel", methods=['GET', 'POST'])
@login_required
@customer_login_required
def cancel_subscription_day(subscription_day_id):

    subscription_day = subscriptionServices.cancel_day(
        subscription_day_id=subscription_day_id)

    return redirect('/customer/subscriptions/'+str(subscription_day.subscription_id))
