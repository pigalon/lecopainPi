from lecopain.dao.models import Order, OrderStatus, Seller
from lecopain.app import app, db
from lecopain.form import OrderForm, OrderShippingDtForm, OrderAnnulationForm
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



#####################################################################
#                                                                   #
#####################################################################
@order_page.route("/orders", methods=['GET', 'POST'])
@login_required
def orders():
    return render_template('/orders/orders.html', title="Commandes")

#####################################################################
#                                                                   #
#####################################################################
@order_page.route("/orders/new", methods=['GET', 'POST'])
@login_required
def order_create():
    form = OrderForm()
    #TODO add lines !!

    lines = (
        request.form.getlist('product_id[]'),
        request.form.getlist('quantity[]'),
        request.form.getlist('price[]'),
    )

    order = {'title': form.title.data,
             'status': form.status.data,
             'customer_id': form.customer_id.data,
             'seller_id': form.seller_id.data,
             'shipping_dt': form.shipping_dt.data,
    }

    if form.validate_on_submit():
        orderServices.create_order_and_parse_line(
            order=order, lines=lines)
        #flash(f'People created for {form.firstname.data}!', 'success')
        return redirect('/orders')

    orderStatusList = orderServices.get_order_status()
    customers = customerService.optim_get_all()

    return render_template('/orders/create_order.html', title='Creation de commande', form=form, customers=customers, orderStatusList=orderStatusList)

#####################################################################
#                                                                   #
#####################################################################
@order_page.route("/orders/<int:order_id>", methods=['GET', 'POST'])
@login_required
def order(order_id):
    order = orderServices.get_one(order_id)
    return render_template('/orders/order.html', order=order)

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
        return redirect('/orders')

    form.customer_id.data = order.customer_id
    form.shipping_dt.data = order.shipping_dt
    form.status.data = order.status
    form.title.data = order.title

    orderStatusList = orderServices.get_order_status()
    return render_template('/orders/update_order.html', order=order, title='Mise à jour de commande', form=form, customer=customer, products=products, selected_products=order.products,  orderStatusList=orderStatusList, line_selection=line_selection)


#####################################################################
#                                                                   #
#####################################################################
@order_page.route("/orders/<int:order_id>/shipping_dt", methods=['GET', 'POST'])
@login_required
def display_update_order_time(order_id):

    order = orderServices.get_one(order_id)
    form = OrderShippingDtForm()

    if form.validate_on_submit():
        orderServices.update_shipping_dt(
            order, shipping_dt=form.shipping_dt.data)
        return redirect('/orders')

    return render_template('/orders/update_shipping_dt.html', order=order, title='Mise a jour du jour de la commande', form=form)

#####################################################################
#                                                                   #
#####################################################################
@order_page.route("/orders/update/<int:order_id>/annulation", methods=['GET', 'POST'])
@login_required
def display_update_order_annulation(order_id):

    orderServices.update_order_status(order_id, 'ANNULEE', None, 'ANNULEE')

    return redirect('/orders')


#####################################################################
#                                                                   #
#####################################################################
@order_page.route("/orders/update/<int:order_id>/created", methods=['GET', 'POST'])
@login_required
def display_update_order_created(order_id):

    orderServices.update_order_status(
        order_id, 'CREE', 'NON_PAYEE', 'NON_LIVREE')

    return redirect('/orders')

#####################################################################
#                                                                   #
#####################################################################
@order_page.route("/orders/update/<int:order_id>/paid", methods=['GET', 'POST'])
@login_required
def display_update_order_paid(order_id):

    orderServices.update_order_status(order_id, None, 'PAYEE', 'NON_LIVREE')

    return redirect('/orders')

#####################################################################
#                                                                   #
#####################################################################
@order_page.route("/orders/update/<int:order_id>/delivered", methods=['GET', 'POST'])
@login_required
def display_update_order_delivered(order_id):

    orderServices.update_order_status(order_id, 'LIVREE', None, 'LIVREE')

    return redirect('/orders')


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
@order_page.route('/api/order/status/')
@login_required
def api_order_status():
    return jsonify({'orders_status': orderServices.get_order_status})

#####################################################################
#                                                                   #
#####################################################################
@order_page.route('/api/orders/count/')
@login_required
def api_order_count():
    total_orders_count = Order.query.count()
    in_progress_orders_count = orderServices.get_in_progess_orders_counter()
    latest_orders_count = orderServices.get_latest_orders_counter()
    return jsonify({'total_orders_count': total_orders_count, 'in_progress_orders_count': in_progress_orders_count})

@order_page.route('/api/orders/')
@login_required
def api_orders():
    return jsonify({'orders': orderServices.get_all()})


@order_page.route('/api/orders/period/<string:period>/customers/<int:customer_id>')
@login_required
def api_day_orders(period, customer_id):
    return jsonify({'orders': orderServices.get_some(period=period, customer_id=customer_id)})
