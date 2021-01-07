from lecopain.services.customer_manager import CustomerManager
from lecopain.app import app
from lecopain.form import PersonForm
from lecopain.helpers.pagination import Pagination
from flask import Blueprint, render_template, request, redirect, url_for, Flask, jsonify
from flask_login import login_required
#import requests
import json
from collections import namedtuple

from lecopain.helpers.roles_utils import admin_login_required
from lecopain.helpers.roles_utils import global_login_required


app = Flask(__name__, instance_relative_config=True)

customerServices = CustomerManager()


customer_page = Blueprint('customer_page', __name__,
                          template_folder='../templates')

#####################################################################
#                                                                   #
#####################################################################
@customer_page.route("/customers", methods=['GET', 'POST'])
@login_required
@admin_login_required
def customers():
    return render_template('/customers/customers.html')

#####################################################################
#                                                                   #
#####################################################################
@customer_page.route("/customers/new", methods=['GET', 'POST'])
@login_required
@admin_login_required
def create_customer():
    form = PersonForm()
    if form.validate_on_submit():
        customerServices.add_customer_form(form)
        #flash(f'People created for {form.firstname.data}!', 'success')
        return redirect('/customers')
    return render_template('/customers/create_customer.html', title='Création du client', form=form)


#####################################################################
#                                                                   #
#####################################################################
@customer_page.route("/customers/<int:customer_id>", methods=['GET', 'POST'])
@login_required
@admin_login_required
def customer(customer_id):
    customer = customerServices.read_one(customer_id)
    customerReports = customerServices.getAllReports(customer_id)
    return render_template('/customers/customer.html', customer=customer, reports=customerReports, title='Clients')

#####################################################################
#                                                                   #
#####################################################################
@customer_page.route("/customers/update/<int:customer_id>", methods=['GET', 'POST'])
@login_required
@admin_login_required
def display_update_order(customer_id):
    customer = customerServices.get_one(customer_id)
    form = PersonForm()

    if form.validate_on_submit():

        customerServices.update_customer_form(customer_id, form)
        #flash(f'People created for {form.firstname.data}!', 'success')
        return redirect(url_for('customer_page.customers'))
    else:
        form.firstname.data = customer.firstname
        form.lastname.data = customer.lastname
        form.email.data = customer.email
        form.address.data = customer.address
        form.cp.data = customer.cp
        form.city.data = customer.city

    return render_template('/customers/update_customer.html', customer=customer, title='Mise a jour de client', form=form)


#####################################################################
#                                                                   #
#####################################################################
@customer_page.route("/customers/delete/<int:customer_id>")
@login_required
@admin_login_required
def display_delete_customer(customer_id):
    customer = customerServices.get_one(customer_id)
    return render_template('/customers/delete_customer.html', customer=customer, title='Suppression de client')

#####################################################################
#                                                                   #
#####################################################################
@customer_page.route("/customers/<int:customer_id>", methods=['DELETE'])
@login_required
@admin_login_required
def delete_customer(customer_id):
    customerServices.delete(id=customer_id)
    return jsonify({})


@customer_page.route('/api/customers/')
@login_required
@global_login_required
def api_customers():
    return jsonify({'customers': customerServices.optim_get_all()})

@customer_page.route('/api/customers/cities')
@login_required
@admin_login_required
def api_cities():
    return jsonify({'cities': customerServices.get_all_cities()})

@customer_page.route('/api/customers/cities/<string:city>')
@login_required
@admin_login_required
def api_customers_cities(city):
    page = request.args.get("page")
    per_page = request.args.get("per_page")

    if page is None:
        page = 1
    if per_page is None:
        per_page=10
    
    data, prev_page, next_page = customerServices.get_all_by_city_pagination(city, page=int(page), per_page=int(per_page))
    
    
    return jsonify(Pagination.get_paginated_db(
        data, '/api/customers/cities/'+city,
        page=request.args.get('page', page),
        per_page=request.args.get('per_page', per_page),
        prev_page=prev_page, next_page=next_page))
    
@customer_page.route('/api/customers/cities/<string:city>/id/<string:customer_id>')
@login_required
@admin_login_required
def api_customers_customer_id(city, customer_id):
    page = request.args.get("page")
    per_page = request.args.get("per_page")

    if page is None:
        page = 1
    if per_page is None:
        per_page=10
        
    customer = customerServices.read_one(customer_id)
    data = [customer]
    prev_page = None
    next_page = None
    
    return jsonify(Pagination.get_paginated_db(
        data, '/api/customers/cities/'+city,
        page=request.args.get('page', page),
        per_page=request.args.get('per_page', per_page),
        prev_page=prev_page, next_page=next_page))
    
@customer_page.route("/api/customers/<int:customer_id>")
@login_required
@global_login_required
def api_customer(customer_id):
    return jsonify({'customer':customerServices.read_one(customer_id)})

