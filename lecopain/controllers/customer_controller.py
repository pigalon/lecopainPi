from lecopain.models import Customer
from lecopain.services.customer_manager import CustomerManager
from lecopain import app, db
from lecopain.form import PersonForm
from flask import Blueprint, render_template, redirect, url_for, Flask, jsonify


app = Flask(__name__, instance_relative_config=True)


customer_page = Blueprint('customer_page', __name__,
                        template_folder='../templates')

@customer_page.route("/customers", methods=['GET', 'POST'])
def customers():
    new_orders=[]
    customerManager = CustomerManager()
    customers = Customer.query.all()
    for customer in customers :
        new_orders.append(customerManager.get_last_order(customer))
    for order in new_orders :
        if order != None :
            print(str(order.order_dt))
    return render_template('/customers/customers.html', customers=customers, new_orders= new_orders, cpt=0)

@customer_page.route("/customers/new", methods=['GET', 'POST'])
def create_customer():
    form = PersonForm()
    if form.validate_on_submit():
        customer = Customer(firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data)
        customer.address = form.address.data
        customer.cp = form.cp.data
        customer.city = form.city.data
        db.session.add(customer)
        db.session.commit()
        #flash(f'People created for {form.firstname.data}!', 'success')
        return redirect(url_for('index'))
    return render_template('/customers/create_customer.html', title='Person form', form=form)

#####################################################################
#                                                                   #
#####################################################################
@customer_page.route("/customers/city/<string:city_name>", methods=['GET', 'POST'])
def customers_by_city(city_name):
   
    new_orders=[]
    customerManager = CustomerManager()
    customers = Customer.query.filter(Customer.city == city_name).all()
    for customer in customers :
        new_orders.append(customerManager.get_last_order(customer))
    for order in new_orders :
        if order != None :
            print(str(order.order_dt))

    return render_template('/customers/customers.html', customers=customers, new_orders= new_orders, cpt=0)

#####################################################################
#                                                                   #
#####################################################################
@customer_page.route("/customers/<int:customer_id>")
def customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return render_template('/customers/customer.html', customer=customer)

#####################################################################
#                                                                   #
#####################################################################
@customer_page.route("/customers/update/<int:customer_id>", methods=['GET', 'POST'])
def display_update_order(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    form = PersonForm()

    if form.validate_on_submit():
        print('update form validate : ' + str(customer.id))

        #order_dt=datetime.strptime('YYYY-MM-DD HH:mm:ss', form.order_dt.data)
        customer.firstname = form.firstname.data
        customer.lastname=form.lastname.data
        customer.email=form.email.data
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
        

    return render_template('/customers/customer_update.html', customer=customer, title='Mise a jour de client', form=form)


#####################################################################
#                                                                   #
#####################################################################
@customer_page.route("/customers/delete/<int:customer_id>")
def display_delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return render_template('/customers/customer_delete.html', customer=customer, title='Suppression de client')

#####################################################################
#                                                                   #
#####################################################################
@customer_page.route("/customers/<int:customer_id>", methods=['DELETE'])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({})
