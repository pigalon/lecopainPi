from lecopain.dao.models import Order, OrderStatus, Seller
from lecopain.app import app, db
from lecopain.form import OrderForm, OrderAnnulationForm
from lecopain.services.order_manager import OrderManager, Period_Enum
from lecopain.services.customer_manager import CustomerManager
from lecopain.services.product_manager import ProductManager

from sqlalchemy import extract
from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, Flask, request, jsonify
from flask_login import login_required

app = Flask(__name__, instance_relative_config=True)

order_page = Blueprint('order_page', __name__,
                       template_folder='../templates')

orderServices = OrderManager()
customerService = CustomerManager()
productService = ProductManager()


def common_display_orders_page(orders, period):
    customers = customerService.optim_get_all()
    map = orderServices.get_maps_from_orders(orders)

    return render_template('/orders/orders.html', customers=customers, orders=orders, map=map, title=f"Commandes - {period}")


#####################################################################
#                                                                   #
#####################################################################
@order_page.route("/orders", methods=['GET', 'POST'])
@login_required
def orders():
    orders = orderServices.all_orders()
    return common_display_orders_page(orders, 'toutes')


#####################################################################
#                                                                   #
#####################################################################
@order_page.route("/orders/month", methods=['GET', 'POST'])
@login_required
def orders_of_current_month():
    orders = orderServices.all_orders(period=Period_Enum.MONTH.value)
    return common_display_orders_page(orders, 'mois')

#####################################################################
#                                                                   #
#####################################################################
@order_page.route("/orders/week", methods=['GET', 'POST'])
@login_required
def orders_of_current_week():
    orders = orderServices.all_orders(period=Period_Enum.WEEK.value)
    return common_display_orders_page(orders, 'semaine')

#####################################################################
#                                                                   #
#####################################################################
@order_page.route("/orders/day", methods=['GET', 'POST'])
@login_required
def orders_of_current_day():
    orders = orderServices.all_orders(period=Period_Enum.DAY.value)
    return common_display_orders_page(orders, 'jour')

#####################################################################
#                                                                   #
#####################################################################
@order_page.route("/orders/customers/<int:customer_id>", methods=['GET', 'POST'])
@login_required
def orders_customer(customer_id):
    orders = orderServices.all_orders(customer_id)
    return common_display_orders_page(orders, 'toutes')

#####################################################################
#                                                                   #
#####################################################################
@order_page.route("/orders/year/<int:year_number>/month/<int:month_number>", methods=['GET', 'POST'])
@login_required
def orders_of_month(year_number, month_number):
    return orders_of_month_by_customer(0, year_number, month_number)

#####################################################################
#                                                                   #
#####################################################################
@order_page.route("/orders/customers/<int:customer_id>/year/<int:year_number>/month/<int:month_number>", methods=['GET', 'POST'])
@login_required
def orders_of_month_by_customer(customer_id, year_number, month_number):

    date_tab = [year_number, month_number, None]
    orders = orderServices.build_orders_list(customer_id, date_tab)

    customers = customerService.optim_get_all()
    map = orderServices.get_maps_from_orders(orders)

    return render_template('/orders/orders.html', customers=customers, orders=orders, map=map, title="Commandes du mois")

#####################################################################
#                                                                   #
#####################################################################
@order_page.route("/orders/year/<int:year_number>/month/<int:month_number>/day/<int:day_number>", methods=['GET', 'POST'])
@login_required
def orders_of_day(year_number, month_number, day_number):

    return orders_of_day_by_customer(0, year_number, month_number, day_number)

#####################################################################
#                                                                   #
#####################################################################
@order_page.route("/orders/customers/<int:customer_id>/year/<int:year_number>/month/<int:month_number>/day/<int:day_number>", methods=['GET', 'POST'])
@login_required
def orders_of_day_by_customer(customer_id, year_number, month_number, day_number):

    date_tab = [year_number, month_number, day_number]
    orders = orderServices.build_orders_list(customer_id, date_tab)

    customers = customerService.optim_get_all()
    map = orderServices.get_maps_from_orders(orders)

    return render_template('/orders/orders.html', customers=customers, orders=orders, map=map, title="Commandes du jour")

#####################################################################
#                                                                   #
#####################################################################
@order_page.route("/orders/resume/year/<int:year_number>/month/<int:month_number>/day/<int:day_number>", methods=['GET', 'POST'])
@login_required
def order_products_of_day(year_number, month_number, day_number):

    date_tab = [year_number, month_number, day_number]
    orders = orderServices.build_orders_list(0, date_tab)

    orders = Order.query.filter(extract('year', Order.shipping_dt) == year_number).filter(extract(
        'month', Order.shipping_dt) == month_number).filter(extract('day', Order.shipping_dt) == day_number).all()
    products_of_day_list = orderServices.get_resume_products_list_from_orders(
        orders)
    customers = customerService.optim_get_all()
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
        order = Order(title=form.title.data, status=form.status.data, customer_id=int(
            form.customer_id.data), shipping_dt=form.shipping_dt.data)
        order = orderServices.create_order(
            order=order, tmp_products=tmp_products, tmp_quantities=tmp_quantities, tmp_prices=tmp_prices)
        db.session.commit()
        #flash(f'People created for {form.firstname.data}!', 'success')
        return redirect('/orders')

    orderStatusList = _get_order_status()
    customers = customerService.optim_get_all()

    return render_template('/orders/create_order.html', title='Creation de commande', form=form, customers=customers, orderStatusList=orderStatusList)

#####################################################################
#                                                                   #
#####################################################################
@order_page.route("/orders/<int:order_id>", methods=['GET', 'POST'])
@login_required
def order(order_id):
    order = Order.query.get_or_404(order_id)

    price, rules = orderServices.calculate_shipping(order)

    customer = customerService.get_one(order.customer_id)
    products = order.products
    products.sort(key=lambda x: x.seller_id, reverse=True)
    sorted_products = sorted(products, key=lambda x: x.seller_id, reverse=True)
    bought_items = order.lines

    return render_template('/orders/order.html', order=order, bought_items=bought_items, products=sorted_products, customer=customer, shipping_price=price, rules=rules)

#####################################################################
#                                                                   #
#####################################################################
@order_page.route("/orders/update/<int:order_id>", methods=['GET', 'POST'])
@login_required
def display_update_order(order_id):

    order = Order.query.get_or_404(order_id)
    form = OrderForm()

    customer = customerService.get_one(order.customer_id)
    products = productService.optim_get_all()

    line_selection = order.lines

    if form.validate_on_submit():
        orderForm = Order(title=form.title.data, status=form.status.data, customer_id=int(
            form.customer_id.data), shipping_dt=form.shipping_dt.data)
        # update order first
        order.status = orderForm.status
        order.shipping_dt = orderForm.shipping_dt
        products = {}

        # get the new list of products and quantities
        tmp_products = request.form.getlist('products')
        tmp_quantities = request.form.getlist('quantities')
        tmp_prices = request.form.getlist('prices')

        orderServices.update_order(
            order=order, products=tmp_products, quantities=tmp_quantities, prices=tmp_prices)

        #flash(f'People created for {form.firstname.data}!', 'success')
        return redirect('/orders/customers/0')

    form.customer_id.data = order.customer_id
    form.shipping_dt.data = order.shipping_dt
    form.status.data = order.status
    form.title.data = order.title

    orderStatusList = _get_order_status()
    return render_template('/orders/update_order.html', order=order, title='Mise a jour de commande', form=form, customer=customer, products=products, selected_products=order.products,  orderStatusList=orderStatusList, line_selection=line_selection)


#####################################################################
#                                                                   #
#####################################################################
@order_page.route("/orders/update/<int:order_id>/time", methods=['GET', 'POST'])
@login_required
def display_update_order_time(order_id):

    order = Order.query.get_or_404(order_id)
    customer = customerService.get_one(order.customer_id)
    form = OrderForm()

    if form.validate_on_submit():
        orderForm = Order(title=form.title.data, status=form.status.data, customer_id=int(
            form.customer_id.data), shipping_dt=form.shipping_dt.data)
        # update order first

        order.shipping_dt = orderForm.shipping_dt

        db.session.commit()

        #flash(f'People created for {form.firstname.data}!', 'success')
        return redirect('/orders/customers/0')

    form.customer_id.data = order.customer_id
    form.shipping_dt.data = order.shipping_dt
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
    order = Order.query.get_or_404(order_id)
    return render_template('/orders/delete_order.html', order=order, title='Suppression de commande')

#####################################################################
#                                                                   #
#####################################################################
@order_page.route("/orders/<int:order_id>", methods=['DELETE'])
@login_required
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)

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
    total_orders_count = Order.query.count()
    in_progress_orders_count = orderServices.get_in_progess_orders_counter()
    latest_orders_count = orderServices.get_latest_orders_counter()
    return jsonify({'total_orders_count': total_orders_count, 'in_progress_orders_count': in_progress_orders_count})
