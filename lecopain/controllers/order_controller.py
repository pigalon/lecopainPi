from lecopain.models import Order, Product, Customer, OrderStatus, Order_product
from lecopain import app, db
from lecopain.form import OrderForm

from sqlalchemy import extract
from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, Flask, request, jsonify

app = Flask(__name__, instance_relative_config=True)


order_page = Blueprint('order_page', __name__,
                        template_folder='../templates')

@order_page.route("/orders", methods=['GET', 'POST'])
def orders():
    orders = Order.query.order_by(Order.order_dt.desc()).all()
    customerMap = {}

    for order in orders :
        customer = Customer.query.get_or_404(order.customer_id)
        customerMap[customer.id] = str(customer.firstname + " " + customer.lastname)
        print("addd : " + customerMap[customer.id])

    for item in customerMap.items() :
        print (str(item))
   
    return render_template('/orders/orders.html', orders=orders, customerMap=customerMap, title="Toutes les commandes")

@order_page.route("/orders/year/<int:year_number>/month/<int:month_number>", methods=['GET', 'POST'])
def orders_of_month(year_number, month_number):
    print(str(datetime.today().month) + " - " + str(datetime.today().day))
    
    if(year_number == 0) :
        year_number = datetime.now().year
    
    if(month_number == 0) :
        month_number = datetime.now().month

    orders = Order.query.filter(extract('year', Order.order_dt) == year_number).filter(extract('month', Order.order_dt) == month_number).all()
    customerMap = {}

    for order in orders :
        customer = Customer.query.get_or_404(order.customer_id)
        customerMap[customer.id] = str(customer.firstname + " " + customer.lastname)
        print("addd : " + customerMap[customer.id])

    for item in customerMap.items() :
        print (str(item))
   
    return render_template('/orders/orders.html', orders=orders, customerMap=customerMap, title="Commandes du mois")

@order_page.route("/orders/year/<int:year_number>/month/<int:month_number>/day/<int:day_number>", methods=['GET', 'POST'])
def orders_of_day(year_number, month_number, day_number):
    print(str(datetime.today().month) + " - " + str(datetime.today().day))
    if(year_number == 0) :
        year_number = datetime.now().year
    
    if(month_number == 0) :
        month_number = datetime.now().month
    
    if(day_number == 0) :
        day_number = datetime.now().month

    orders = Order.query.filter(extract('year', Order.order_dt) == year_number).filter(extract('month', Order.order_dt) == month_number).filter(extract('day', Order.order_dt) == day_number).all()
    
    customerMap = {}

    for order in orders :
        customer = Customer.query.get_or_404(order.customer_id)
        customerMap[customer.id] = str(customer.firstname + " " + customer.lastname)
        print("addd : " + customerMap[customer.id])

    for item in customerMap.items() :
        print (str(item))
   
    return render_template('/orders/orders.html', orders=orders, customerMap=customerMap, title="Commandes du jour")



@order_page.route("/orders/new", methods=['GET', 'POST'])
def order_create():
    form = OrderForm()
    tmp_products = request.form.getlist('products')
    tmp_quantity = request.form.getlist('quantities')

    for i in range(0,len(tmp_products)):
            product = Product.query.get(tmp_products[i])

    if form.validate_on_submit():

        #order_dt=datetime.strptime('YYYY-MM-DD HH:mm:ss', form.order_dt.data)
        order = Order(title=form.title.data, status=form.status.data, customer_id=int(form.customer_id.data), order_dt=form.order_dt.data)
        products = {}

        for i in range(0,len(tmp_products)): 
            product = Product.query.get(tmp_products[i])
            order.selected_products.append(product)

        db.session.add(order)
        db.session.commit()

        for i in range(0,len(tmp_products)):
            bought_item = Order_product.query.filter(Order_product.order_id == order.id).filter(Order_product.product_id == tmp_products[i]).first()
            bought_item.quantity = tmp_quantity[i]
            bought_item.price = order.selected_products[i].price
 
        db.session.commit()
        
        #flash(f'People created for {form.firstname.data}!', 'success')
        return redirect(url_for('order_page.orders'))
    else:
        customers = Customer.query.all()
        products = Product.query.all()
    #else:
    #    flash(f'Failed!', 'danger')
    orderStatusList = _get_order_status()

    return render_template('/orders/create_order.html', title='order form', form=form, customers=customers, products=products, orderStatusList=orderStatusList)


@order_page.route("/orders/<int:order_id>", methods=['GET', 'POST'])
def order(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('/orders/order.html', order=order)

@order_page.route("/orders/update/<int:order_id>")
def display_update_order(order_id):
    order = Order.query.get_or_404(order_id)
    form = OrderForm()
    form.customer_id.data = order.customer_id
    form.order_dt.data = order.order_dt
    form.status.data = order.status
    form.title.data = order.title
    

    tmp_products = request.form.getlist('products')
    tmp_quantity = request.form.getlist('quantities')

    for i in range(0,len(tmp_products)):
        product = Product.query.get(tmp_products[i])

    customers = Customer.query.all()
    products = Product.query.all()
    orderStatusList = _get_order_status()
    return render_template('/orders/order_update.html', order=order, title='order form', form=form, customers=customers, products=products, selected_products=order.selected_products,  orderStatusList=orderStatusList)

@order_page.route("/orders/delete/<int:order_id>")
def display_delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('/orders/order_delete.html', order=order)

@order_page.route("/orders/<int:order_id>", methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({})

@app.route('/_get_order_status/')
def _get_order_status():
    ordersStatusList = [(row.name) for row in OrderStatus.query.all()]
    return ordersStatusList