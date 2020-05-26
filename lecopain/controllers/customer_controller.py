from lecopain.dao.models import Customer
from lecopain.services.customer_manager import CustomerManager
from lecopain.app import app, db
from lecopain.form import PersonForm
from flask import Blueprint, render_template, redirect, url_for, Flask, jsonify
from flask_login import login_required
import requests
import json
from collections import namedtuple


app = Flask(__name__, instance_relative_config=True)

customerServices = CustomerManager()


customer_page = Blueprint('customer_page', __name__,
                          template_folder='../templates')

#####################################################################
#                                                                   #
#####################################################################
@customer_page.route("/customers", methods=['GET', 'POST'])
@login_required
def customers():
    return render_template('/customers/customers.html')

#####################################################################
#                                                                   #
#####################################################################
@customer_page.route("/customers/new", methods=['GET', 'POST'])
@login_required
def create_customer():
    form = PersonForm()
    if form.validate_on_submit():
        customer = Customer(firstname=form.firstname.data,
                            lastname=form.lastname.data, email=form.email.data)
        customer.address = form.address.data
        customer.cp = form.cp.data
        customer.city = form.city.data
        db.session.add(customer)
        db.session.commit()
        #flash(f'People created for {form.firstname.data}!', 'success')
        return redirect('/customers')
    return render_template('/customers/create_customer.html', title='Person form', form=form)


#####################################################################
#                                                                   #
#####################################################################
@customer_page.route("/customers/<int:customer_id>")
@login_required
def customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return render_template('/customers/customer.html', customer=customer)

#####################################################################
#                                                                   #
#####################################################################
@customer_page.route("/customers/update/<int:customer_id>", methods=['GET', 'POST'])
@login_required
def display_update_order(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    form = PersonForm()

    if form.validate_on_submit():
        print('update form validate : ' + str(customer.id))

        #shipping_dt=datetime.strptime('YYYY-MM-DD HH:mm:ss', form.shipping_dt.data)
        customer.firstname = form.firstname.data
        customer.lastname = form.lastname.data
        customer.email = form.email.data
        customer.address = form.address.data
        customer.cp = form.cp.data
        customer.city = form.city.data

        db.session.commit()

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
def display_delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return render_template('/customers/delete_customer.html', customer=customer, title='Suppression de client')

#####################################################################
#                                                                   #
#####################################################################
@customer_page.route("/customers/<int:customer_id>", methods=['DELETE'])
@login_required
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({})


@customer_page.route('/api/customers/')
@login_required
def api_customers():
    return jsonify({'customers': customerServices.optim_get_all()})

@customer_page.route('/api/customers/cities')
@login_required
def api_cities():
    return jsonify({'cities': customerServices.get_all_cities()})

@customer_page.route('/api/customers/cities/<string:city>')
@login_required
def api_customers_cities(city):
    return jsonify({'customers': customerServices.get_all_by_city(city)})