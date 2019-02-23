from flask import render_template, url_for,  flash, redirect, jsonify

from lecopain import app, db

from datetime import datetime

from lecopain.form import PersonForm, OrderForm
from lecopain.models import Customer, Order

customers2 = [
    {
        'id':1,
        'firstname': 'Jean',
        'lastname':'Delatour',
        'email':'jean.delatour@gmail.com',
        'address':'30 Rue Haute',
        'cp':'30413',
        'city':'Langlade'
    },
    {
        'id':2,
        'firstname': 'Suzanne',
        'lastname':'Vega',
        'email':'suzanne.vega@gmail.com',
        'address':'58 Rue de Barcelone',
        'cp':'30000',
        'city':'Nimes'
    }
]



@app.route("/")
@app.route("/home")
def index():
    customers = Customer.query.all()
    return render_template('index.html', customers=customers)


@app.route("/customers", methods=['GET', 'POST'])
def about():
   customers = Customer.query.all()
   return render_template('/customers/customers.html', customers=customers)

@app.route("/customers/new", methods=['GET', 'POST'])
def create_customer():
    form = PersonForm()
    if form.validate_on_submit():
        customer = Customer(firstname=form.firstname.data, lastname=form.lastname.data, email=form.email.data)
        db.session.add(customer)
        db.session.commit()
        #flash(f'People created for {form.firstname.data}!', 'success')
        return redirect(url_for('index'))
    return render_template('/customers/create_customer.html', title='Person form', form=form)

@app.route("/orders", methods=['GET', 'POST'])
def order():
    form = OrderForm()
    
    if form.validate_on_submit():
        #order_dt=datetime.strptime('YYYY-MM-DD HH:mm:ss', form.order_dt.data)
        #printf('oder : ' + str(order_dt))
        #order = Order(title=form.title.data, customer_id=int(form.customer_id.data), order_dt=datetime(form.order_dt.data))
        order = Order(title=form.title.data, customer_id=int(form.customer_id.data), order_dt=form.order_dt.data)
        
        db.session.add(order)
        db.session.commit()
        #flash(f'People created for {form.firstname.data}!', 'success')
        return redirect(url_for('index'))
    else:
        customers = Customer.query.all()
    #else:
    #    flash(f'Failed!', 'danger')
    return render_template('order.html', title='order form', form=form, customers=customers)

@app.route('/_get_customers/')
def _get_customers():
    customers = [(row.id, row.firstname) for row in Customer.query.all()]
    return jsonify(customers)


if __name__ == '__main__':
    app.run(debug=True)

