from lecopain.dao.models import Customer, CustomerOrder, Product, OrderStatus, Line, Delivery, VendorOrder
from lecopain import app, db
from lecopain.form import OrderForm, OrderAnnulationForm
from lecopain.services.order_manager import OrderManager

from sqlalchemy import extract
from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, Flask, request, jsonify
from flask_login import login_required

app = Flask(__name__, instance_relative_config=True)

order_page = Blueprint('order_page', __name__,
                       template_folder='../templates')

orderServices = OrderManager()


#####################################################################
#                                                                   #
#####################################################################
@order_page.route("/orders/customers/<int:customer_id>", methods=['GET', 'POST'])
@login_required
def orders(customer_id):

    if customer_id == 0 or customer_id == None:

        orders = CustomerOrder.query.order_by(
            CustomerOrder.delivery_dt.desc()).all()
    else:
        orders = CustomerOrder.query.filter(CustomerOrder.customer_id == customer_id).order_by(
            CustomerOrder.delivery_dt.desc()).all()

    customers = Customer.query.all()
    map = orderServices.get_maps_from_orders(orders)

    return render_template('/orders/orders.html', orders=orders, customers=customers, title="Toutes les commandes", map=map)

#####################################################################
#                                                                   #
#####################################################################
@order_page.route("/orders/customers/<int:customer_id>/year/<int:year_number>/month/<int:month_number>", methods=['GET', 'POST'])
@login_required
def orders_of_month(customer_id, year_number, month_number):

    if(year_number == 0):
        year_number = datetime.now().year

    if(month_number == 0):
        month_number = datetime.now().month

    if customer_id == 0 or customer_id == None:
        orders = CustomerOrder.query.filter(extract('year', CustomerOrder.delivery_dt) == year_number).filter(
            extract('month', CustomerOrder.delivery_dt) == month_number).all()
    else:
        orders = CustomerOrder.query.filter(CustomerOrder.customer_id == customer_id).filter(
            extract('year', CustomerOrder.delivery_dt) == year_number).filter(
            extract('month', CustomerOrder.delivery_dt) == month_number).all()

    customers = Customer.query.all()
    map = orderServices.get_maps_from_orders(orders)

    return render_template('/orders/orders.html', customers=customers, orders=orders, map=map, title="Commandes du mois")

#####################################################################
#                                                                   #
#####################################################################
@order_page.route("/orders/customers/<int:customer_id>/year/<int:year_number>/month/<int:month_number>/day/<int:day_number>", methods=['GET', 'POST'])
@login_required
def orders_of_day(customer_id, year_number, month_number, day_number):
    if(year_number == 0):
        year_number = datetime.now().year

    if(month_number == 0):
        month_number = datetime.now().month

    if(day_number == 0):
        day_number = datetime.now().day

    if customer_id == 0 or customer_id == None:
        orders = CustomerOrder.query.filter(extract('year', CustomerOrder.delivery_dt) == year_number).filter(
            extract('month', CustomerOrder.delivery_dt) == month_number).filter(
            extract('day', CustomerOrder.delivery_dt) == day_number).all()
    else:
        orders = CustomerOrder.query.filter(CustomerOrder.customer_id == customer_id).filter(
            extract('year', CustomerOrder.delivery_dt) == year_number).filter(
            extract('month', CustomerOrder.delivery_dt) == month_number).filter(
            extract('day', CustomerOrder.delivery_dt) == day_number).all()

    customers = Customer.query.all()
    map = orderServices.get_maps_from_orders(orders)

    return render_template('/orders/orders.html', customers=customers, orders=orders, map=map, title="Commandes du jour")


#####################################################################
#                                                                   #
#####################################################################
@order_page.route("/orders/resume/customers/<int:customer_id>/year/<int:year_number>/month/<int:month_number>/day/<int:day_number>", methods=['GET', 'POST'])
@login_required
def order_products_of_day(customer_id, year_number, month_number, day_number):
    if(year_number == 0):
        year_number = datetime.now().year

    if(month_number == 0):
        month_number = datetime.now().month

    if(day_number == 0):
        day_number = datetime.now().month

    if customer_id == 0 or customer_id == None:
        orders = CustomerOrder.query.filter(extract('year', CustomerOrder.delivery_dt) == year_number).filter(
            extract('month', CustomerOrder.delivery_dt) == month_number).filter(
            extract('day', CustomerOrder.delivery_dt) == day_number).all()
    else:
        orders = CustomerOrder.query.filter(CustomerOrder.customer_id == customer_id).filter(
            extract('year', CustomerOrder.delivery_dt) == year_number).filter(
            extract('month', CustomerOrder.delivery_dt) == month_number).filter(
            extract('day', CustomerOrder.delivery_dt) == day_number).all()

    orders = CustomerOrder.query.filter(extract('year', CustomerOrder.delivery_dt) == year_number).filter(extract(
        'month', CustomerOrder.delivery_dt) == month_number).filter(extract('day', CustomerOrder.delivery_dt) == day_number).all()
    products_of_day_list = orderServices.get_resume_products_list_from_orders(
        orders)
    customers = Customer.query.all()
    map = orderServices.get_maps_from_orders(orders)

    return render_template('/orders/orders_by_day.html', orders=orders, map=map, bought_products=products_of_day_list, title="Commandes du jour")


#####################################################################
#                                                                   #
#####################################################################
@order_page.route("/orders/new", methods=['GET', 'POST'])
@login_required
def order_create():
    form = OrderForm()
    tmp_products = request.form.getlist('products')
    tmp_quantities = request.form.getlist('quantities')
    tmp_prices = request.form.getlist('prices')

    if form.validate_on_submit():
        order = CustomerOrder(title=form.title.data, status=form.status.data, customer_id=int(
            form.customer_id.data), delivery_dt=form.delivery_dt.data)
        orderServices.create_customer_order(
            order=order, tmp_products=tmp_products, tmp_quantities=tmp_quantities, tmp_prices=tmp_prices)
        #flash(f'People created for {form.firstname.data}!', 'success')
        redirect('/orders/customers/0')

    products = Product.query.all()
    orderStatusList = _get_order_status()
    customers = Customer.query.all()

    return render_template('/orders/create_order.html', title='Creation de commande', form=form, customers=customers, products=products, orderStatusList=orderStatusList)

#####################################################################
#                                                                   #
#####################################################################
@order_page.route("/orders/<int:order_id>", methods=['GET', 'POST'])
@login_required
def order(order_id):
    order = CustomerOrder.query.get_or_404(order_id)

    price, rules = orderServices.calculate_delivery(order)

    customer = Customer.query.get_or_404(order.customer_id)
    products = order.selected_products
    products.sort(key=lambda x: x.vendor_id, reverse=True)
    sorted_products = sorted(products, key=lambda x: x.vendor_id, reverse=True)
    bought_items = Line.query.filter(
        Line.order_id == order.id).all()

    return render_template('/orders/order.html', order=order, bought_items=bought_items, products=sorted_products, customer=customer, delivery_price=price, rules=rules)

#####################################################################
#                                                                   #
#####################################################################
@order_page.route("/orders/update/<int:order_id>", methods=['GET', 'POST'])
@login_required
def display_update_order(order_id):

    order = CustomerOrder.query.get_or_404(order_id)
    form = OrderForm()

    customer = Customer.query.get_or_404(order.customer_id)
    products = Product.query.all()

    line_selection = Line.query.filter(
        Line.order_id == order.id).all()

    if form.validate_on_submit():
        orderForm = CustomerOrder(title=form.title.data, status=form.status.data, customer_id=int(
            form.customer_id.data), delivery_dt=form.delivery_dt.data)
        # update order first
        order.status = orderForm.status
        order.delivery_dt = orderForm.delivery_dt
        products = {}

        # get the new list of products and quantities
        tmp_products = request.form.getlist('products')
        tmp_quantities = request.form.getlist('quantities')
        tmp_prices = request.form.getlist('prices')

        orderServices.update_customer_order(
            order=order, products=tmp_products, quantities=tmp_quantities, prices=tmp_prices)

        #flash(f'People created for {form.firstname.data}!', 'success')
        return redirect('/orders/customers/0')

    form.customer_id.data = order.customer_id
    form.delivery_dt.data = order.delivery_dt
    form.status.data = order.status
    form.title.data = order.title

    orderStatusList = _get_order_status()
    return render_template('/orders/update_order.html', order=order, title='Mise a jour de commande', form=form, customer=customer, products=products, selected_products=order.selected_products,  orderStatusList=orderStatusList, line_selection=line_selection)


#####################################################################
#                                                                   #
#####################################################################
@order_page.route("/orders/update/<int:order_id>/time", methods=['GET', 'POST'])
@login_required
def display_update_order_time(order_id):

    order = CustomerOrder.query.get_or_404(order_id)
    customer = Customer.query.get_or_404(order.customer_id)
    form = OrderForm()

    if form.validate_on_submit():
        orderForm = CustomerOrder(title=form.title.data, status=form.status.data, customer_id=int(
            form.customer_id.data), delivery_dt=form.delivery_dt.data)
        # update order first

        order.delivery_dt = orderForm.delivery_dt

        delivery = Delivery.query.filter(
            Delivery.customer_order_id == order.id).first()
        delivery.delivery_dt = orderForm.delivery_dt

        db.session.commit()

        #flash(f'People created for {form.firstname.data}!', 'success')
        return redirect('/orders/customers/0')

    form.customer_id.data = order.customer_id
    form.delivery_dt.data = order.delivery_dt
    form.status.data = order.status
    form.title.data = order.title

    orderStatusList = _get_order_status()
    return render_template('/orders/update_time.html', customer=customer, order=order, title='Mise a jour du jour de la commande', form=form)

#####################################################################
#                                                                   #
#####################################################################
@order_page.route("/orders/update/<int:order_id>/annulation", methods=['GET', 'POST'])
@login_required
def display_update_order_annulation(order_id):

    orderServices.update_order_status(order_id, 'ANNULEE', None, 'ANNULEE')

    return redirect('/orders/customers/0')


#####################################################################
#                                                                   #
#####################################################################
@order_page.route("/orders/update/<int:order_id>/created", methods=['GET', 'POST'])
@login_required
def display_update_order_created(order_id):

    orderServices.update_order_status(
        order_id, 'CREE', 'NON_PAYEE', 'NON_LIVREE')

    return redirect('/orders/customers/0')

#####################################################################
#                                                                   #
#####################################################################
@order_page.route("/orders/update/<int:order_id>/paid", methods=['GET', 'POST'])
@login_required
def display_update_order_paid(order_id):

    orderServices.update_order_status(order_id, None, 'PAYEE', 'NON_LIVREE')

    return redirect('/orders/customers/0')

#####################################################################
#                                                                   #
#####################################################################
@order_page.route("/orders/update/<int:order_id>/delivered", methods=['GET', 'POST'])
@login_required
def display_update_order_delivered(order_id):

    orderServices.update_order_status(order_id, 'LIVREE', None, 'LIVREE')

    return redirect('/orders/customers/0')


#####################################################################
#                                                                   #
#####################################################################
@order_page.route("/orders/delete/<int:order_id>")
@login_required
def display_delete_order(order_id):
    order = CustomerOrder.query.get_or_404(order_id)
    return render_template('/orders/delete_order.html', order=order, title='Suppression de commande')

#####################################################################
#                                                                   #
#####################################################################
@order_page.route("/orders/<int:order_id>", methods=['DELETE'])
@login_required
def delete_order(order_id):
    order = CustomerOrder.query.get_or_404(order_id)

    delivery = Delivery.query.filter(
        Delivery.customer_order_id == order_id).first()
    if delivery != None:
        db.session.delete(delivery)

    vendorOrders = VendorOrder.query.filter(
        VendorOrder.customer_order_id == order_id).all()
    for vendorOrder in vendorOrders:
        db.session.delete(vendorOrder)

    db.session.delete(order)
    db.session.commit()
    return jsonify({})

#####################################################################
#                                                                   #
#####################################################################
@order_page.route('/_get_order_status/')
@login_required
def _get_order_status():
    ordersStatusList = [(row.name) for row in OrderStatus.query.all()]
    return ordersStatusList

#####################################################################
#                                                                   #
#####################################################################
@order_page.route('/_getjs_order_status/')
@login_required
def _getjs_order_status():
    ordersStatusList = [(row.name) for row in OrderStatus.query.all()]
    return jsonify({'orders_status': ordersStatusList})

#####################################################################
#                                                                   #
#####################################################################
@order_page.route('/_getjs_order_count/')
@login_required
def _getjs_order_count():
    total_orders_count = CustomerOrder.query.count()
    in_progress_orders_count = orderServices.get_in_progess_orders_counter()
    latest_orders_count = orderServices.get_latest_orders_counter()
    return jsonify({'total_orders_count': total_orders_count, 'in_progress_orders_count': in_progress_orders_count})
