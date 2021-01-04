from lecopain.dao.models import Subscription, Product, Customer
from lecopain.app import app, db
from lecopain.form import SubscriptionForm, SubscriptionDayForm
from lecopain.services.subscription_manager import SubscriptionManager
from lecopain.services.customer_manager import CustomerManager
from lecopain.services.seller_manager import SellerManager
from lecopain.helpers.pagination import Pagination
from lecopain.helpers.date_utils import get_week_names

from sqlalchemy import extract
from datetime import datetime


from flask import Blueprint, render_template, redirect, url_for, Flask, request, jsonify
from flask_login import login_required

from lecopain.helpers.roles_utils import admin_login_required

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
@admin_login_required
def subscriptions():
  return render_template('/subscriptions/subscriptions.html', title="Abonnements")

#####################################################################
#                                                                   #
#####################################################################
@subscription_page.route("/subscriptions/<int:subscription_id>", methods=['GET', 'POST'])
@login_required
@admin_login_required
def subscription(subscription_id):
  subscription = subscriptionServices.get_one(subscription_id)
  week_days = get_week_names()
  return render_template('/subscriptions/subscription.html', subscription=subscription, week_days=week_days)

#####################################################################
#                                                                   #
#####################################################################
@subscription_page.route('/api/subscriptions/')
@login_required
@admin_login_required
def api_subscriptions():
  return jsonify({'subscriptions': subscriptionServices.get_all()})

#####################################################################
#                                                                   #
#####################################################################
@subscription_page.route('/api/subscriptions/customers/<int:customer_id>')
@login_required
@admin_login_required
def api_subscriptions_by_customer(customer_id):
  return jsonify({'subscriptions': subscriptionServices.get_all_by_customer(customer_id)})

#####################################################################
#                                                                   #
#####################################################################
@subscription_page.route('/api/subscriptions/sellers/<int:seller_id>')
@login_required
@admin_login_required
def api_subscriptions_by_seller(seller_id):
  return jsonify({'subscriptions': subscriptionServices.get_all_by_seller(seller_id)})

#####################################################################
#                                                                   #
#####################################################################
@subscription_page.route('/api/subscriptions/period/<string:period>/date/<string:day>/customers/<int:customer_id>')
@login_required
@admin_login_required
def api_day_subscriptions(period, day, customer_id):
	
	page = request.args.get("page")
	per_page = request.args.get("per_page")

	if page is None:
		page = 1
	if per_page is None:
		per_page=10
	
	data, prev_page, next_page = subscriptionServices.get_some_pagination(period=period, day=day, 
                                            customer_id=customer_id, page=int(page), per_page=int(per_page))
	
	return jsonify(Pagination.get_paginated_db(
		data, '/api/subscriptions/period/'+period+'/date/'+day+'/customers/'+str(customer_id),
		page=request.args.get('page', page),
		per_page=request.args.get('per_page', per_page),
		prev_page=prev_page, next_page=next_page))

#####################################################################
#                                                                   #
#####################################################################
@subscription_page.route("/subscriptions/new", methods=['GET', 'POST'])
@login_required
@admin_login_required
def subscription_create():
	form = SubscriptionForm()

	subscription = {
		'customer_id': form.customer_id.data,
		'start_dt': form.start_dt.data,
		'end_dt': form.end_dt.data,
	}
	
	subscription_id = request.args.get("subscription_id")

	if form.validate_on_submit():
		if subscription_id is not None:
			subscriptionServices.duplicate_subscription(subscription_id=int(subscription_id),
			subscription=subscription)
		else:
			subscriptionServices.create_subscription(
			subscription=subscription)
		return redirect('/subscriptions')

	sellers = sellerServices.optim_get_all()
	
	if subscription_id is not None:
		customers = []
		subscription = subscriptionServices.get_one_db(int(subscription_id))
		customers.append(subscription.customer)
	else:
		customers = customerServices.optim_get_all()

	return render_template('/subscriptions/create_subscription.html', title="Creation d'abonnement", 
                        form=form, customers=customers, sellers=sellers)

#####################################################################
#                                                                   #
#####################################################################
@subscription_page.route("/subscriptions/delete/<int:subscription_id>")
@login_required
@admin_login_required
def display_delete_subscription(subscription_id):
	subscription = subscriptionServices.get_one(subscription_id)
	return render_template('/subscriptions/delete_subscription.html', subscription=subscription, title="Suppression d'abonnement")

#####################################################################
#                                                                   #
#####################################################################
@subscription_page.route("/subscriptions/<int:subscription_id>", methods=['DELETE'])
@login_required
@admin_login_required
def delete_subscription(subscription_id):
	subscriptionServices.delete_subscription(subscription_id)
	return jsonify({})

#####################################################################
#                                                                   #
#####################################################################
@subscription_page.route("/subscriptions/generate/<int:subscription_id>")
@login_required
@admin_login_required
def generate_shipments(subscription_id):
	subscription = subscriptionServices.get_one_db(subscription_id)
	if len(subscription.shipments)<1 :
		subscriptionServices.generate_shipments(subscription)
	week_days = get_week_names()
	return render_template('/subscriptions/subscription.html', subscription=subscription, week_days=week_days)

#####################################################################
#                                                                   #
#####################################################################
@subscription_page.route("/subscriptions/calculation/<int:subscription_id>")
@login_required
@admin_login_required
def calculatee_shipments(subscription_id):
  subscription = subscriptionServices.get_one_db(subscription_id)
  subscriptionServices.calculate(subscription)
  week_days = get_week_names()
  return render_template('/subscriptions/subscription.html', subscription=subscription, week_days=week_days)

#####################################################################
#                                                                   #
#####################################################################
@subscription_page.route("/subscriptions/delete_shipments/<int:subscription_id>")
@login_required
@admin_login_required
def delete_shipments(subscription_id):
	subscription = subscriptionServices.get_one_db(subscription_id)
	subscriptionServices.delete_all_shipments(subscription)
	week_days = get_week_names()
	return render_template('/subscriptions/subscription.html', subscription=subscription, week_days=week_days)

#####################################################################
#                                                                   #
#####################################################################
@subscription_page.route("/subscriptions/days/<int:subscription_day_id>", methods=['GET', 'POST'])
@login_required
@admin_login_required
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
		return redirect('/subscriptions/'+str(subscription_day.get('subscription')))

	return render_template('/subscriptions/subscription_day.html', form=form, subscription_day=subscription_day)

#####################################################################
#                                                                   #
#####################################################################
@subscription_page.route("/subscriptions/<int:subscription_id>/weekdays/<int:week_day>", methods=['GET', 'POST'])
@login_required
@admin_login_required
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
		return redirect('/subscriptions/'+str(subscription_day.get('subscription')))

	return render_template('/subscriptions/subscription_day.html', form=form, subscription_day=subscription_day)


#####################################################################
#                                                                   #
#####################################################################
@subscription_page.route("/subscriptions/days/<int:subscription_day_id>/cancel", methods=['GET', 'POST'])
@login_required
@admin_login_required
def cancel_subscription_day(subscription_day_id):

	subscription_day = subscriptionServices.cancel_day(
		subscription_day_id=subscription_day_id)

	return redirect('/subscriptions/'+str(subscription_day.subscription_id))
