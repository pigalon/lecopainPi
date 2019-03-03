from lecopain.models import Order, Product, Customer
from lecopain import app, db
from lecopain.form import OrderForm

from flask import Blueprint, render_template, redirect, url_for, Flask, request

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

@order_page.route("/orders/month/<int:month_number>", methods=['GET', 'POST'])
def orders_of_month(month_number):
    orders = Order.query.all()
    customerMap = {}

    for order in orders :
        customer = Customer.query.get_or_404(order.customer_id)
        customerMap[customer.id] = str(customer.firstname + " " + customer.lastname)
        print("addd : " + customerMap[customer.id])

    for item in customerMap.items() :
        print (str(item))
   
    return render_template('/orders/orders.html', orders=orders, customerMap=customerMap, title="Commandes du mois")

@order_page.route("/orders/new", methods=['GET', 'POST'])
def order_create():
    form = OrderForm()
    tmp_products = request.form.getlist('products')
    tmp_quantity = request.form.getlist('quantities')
    
    #print("type :"+ str( len(tmp_products)) + str(tmp_products[0]))

    for i in range(0,len(tmp_products)):
            product = Product.query.get(tmp_products[i])
            print(str(product))
            print(str(tmp_quantity[i]))

    if form.validate_on_submit():

        #order_dt=datetime.strptime('YYYY-MM-DD HH:mm:ss', form.order_dt.data)
        order = Order(title=form.title.data, status=form.status.data, customer_id=int(form.customer_id.data), order_dt=form.order_dt.data)
        products = {}

        for i in range(0,len(tmp_products)): 
            product = Product.query.get(tmp_products[i])
            order.selected_products.append(product)

        for i in range(0,len(tmp_products)):
            print('tmp_quantity : ' + str(tmp_quantity[i]))
            print('selected : ' + str(order.selected_products[i]))
        
        print('order : ' + str(order))

        db.session.add(order)
        db.session.commit()
        print('order id : ' + str(order.id))

        for i in range(0,len(tmp_products)):
            bought_items = Order_product.query.filter(Order_product.order_id == order.id).filter(Order_product.product_id == tmp_products[i]).first()
            bought_items.quantity = tmp_quantity[i]
 
        db.session.commit()
        
        #flash(f'People created for {form.firstname.data}!', 'success')
        return redirect(url_for('index'))
    else:
        customers = Customer.query.all()
        products = Product.query.all()
    #else:
    #    flash(f'Failed!', 'danger')
    orderStatusList = _get_order_status()


    return render_template('/orders/create_order.html', title='order form', form=form, customers=customers, products=products, orderStatusList=orderStatusList)

@order_page.route("/orders/<int:order_id>")
def order(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('/orders/order.html', order=order)