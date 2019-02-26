from flask import render_template, url_for,  flash, redirect, jsonify

from lecopain import app, db

from datetime import datetime

from lecopain.form import PersonForm, OrderForm
from lecopain.models import Customer, Order, OrderStatus

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
def customers():
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

@app.route("/customers/<int:customer_id>")
def customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return render_template('/customers/customer.html', customer=customer)

@app.route("/orders", methods=['GET', 'POST'])
def orders():
    orders = Order.query.all()
    customerMap = {}

    for order in orders :
        customer = Customer.query.get_or_404(order.customer_id)
        customerMap[customer.id] = str(customer.firstname + " " + customer.lastname)
        print("addd : " + customerMap[customer.id])

    for item in customerMap.items() :
        print (str(item))
   
    return render_template('/orders/orders.html', orders=orders, customerMap=customerMap)

@app.route("/orders/new", methods=['GET', 'POST'])
def order_create():
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
    orderStatusList = _get_order_status()

    return render_template('order.html', title='order form', form=form, customers=customers, orderStatusList=orderStatusList)

@app.route("/orders/<int:order_id>")
def order(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('/orders/order.html', order=order)


@app.route('/_get_customers/')
def _get_customers():
    customers = [(row.id, row.firstname) for row in Customer.query.all()]
    return jsonify(customers)

@app.route('/_get_order_status/')
def _get_order_status():
    ordersStatusList = [(row.name) for row in OrderStatus.query.all()]
    return ordersStatusList


if __name__ == '__main__':
    app.run(debug=True)

