from lecopain.dao.models import OrderStatus_Enum,  OrderStatus, ShippingStatus_Enum, PaymentStatus_Enum
from lecopain.app import app
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
@order_page.route("/orders/<int:order_id>/cancel", methods=['GET', 'POST'])
@login_required
def display_update_order_annulation(order_id):
    orderServices.update_order_status(order_id, OrderStatus_Enum.ANNULEE.value)
    return redirect('/orders')

#####################################################################
#                                                                   #
#####################################################################

@order_page.route("/orders/<int:order_id>/created", methods=['GET', 'POST'])
@login_required
def display_update_order_created(order_id):
    orderServices.update_order_status(order_id, OrderStatus_Enum.CREE.value)
    return redirect('/orders')

#####################################################################
#                                                                   #
#####################################################################

@order_page.route("/orders/<int:order_id>/shipped/<string:status>", methods=['GET', 'POST'])
@login_required
def update_order_shipped(order_id, status):
    if status == 'NON':
        orderServices.update_order_shipping_status(order_id, ShippingStatus_Enum.NON.value)
    else:
        orderServices.update_order_shipping_status(order_id, ShippingStatus_Enum.OUI.value)
    return redirect('/orders')

#####################################################################
#                                                                   #
#####################################################################


@order_page.route("/orders/<int:order_id>/paid/<string:status>", methods=['GET', 'POST'])
@login_required
def update_order_paid(order_id, status):
    if status == 'NON':
        orderServices.update_order_payment_status(
            order_id, PaymentStatus_Enum.NON.value)
    else:
        orderServices.update_order_payment_status(
            order_id, PaymentStatus_Enum.OUI.value)
    return redirect('/orders')


#####################################################################
#                                                                   #
#####################################################################
@order_page.route("/orders/delete/<int:order_id>")
@login_required
def display_delete_order(order_id):
    order = orderServices.get_one(order_id)
    return render_template('/orders/delete_order.html', order=order, title='Suppression de commande')

#####################################################################
#                                                                   #
#####################################################################
@order_page.route("/orders/<int:order_id>", methods=['DELETE'])
@login_required
def delete_order(order_id):
    orderServices.delete_order(order_id)
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
@order_page.route('/api/orders/')
@login_required
def api_orders():
    return jsonify({'orders': orderServices.get_all()})

#####################################################################
#                                                                   #
#####################################################################
@order_page.route('/api/orders/period/<string:period>/customers/<int:customer_id>')
@login_required
def api_day_orders(period, customer_id):
    return jsonify({'orders': orderServices.get_some(period=period, customer_id=customer_id)})
