from lecopain.dao.models import ShipmentStatus_Enum,  ShippingStatus_Enum, PaymentStatus_Enum
from lecopain.app import app
from lecopain.form import ShipmentForm, ShippingDtForm, CancellationForm
from lecopain.services.shipment_manager import ShipmentManager, Period_Enum
from lecopain.services.customer_manager import CustomerManager
from lecopain.services.product_manager import ProductManager

from sqlalchemy import extract
from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, Flask, request, jsonify
from flask_login import login_required

app = Flask(__name__, instance_relative_config=True)

shipment_page = Blueprint('shipment_page', __name__,
                       template_folder='../templates')

shipmentServices = ShipmentManager()
customerService = CustomerManager()
productService = ProductManager()



#####################################################################
#                                                                   #
#####################################################################
@shipment_page.route("/shipments", methods=['GET', 'POST'])
@login_required
def shipments():
    return render_template('/shipments/shipments.html', title="Livraisons")

#####################################################################
#                                                                   #
#####################################################################
@shipment_page.route("/shipments/new", methods=['GET', 'POST'])
@login_required
def shipment_create():
    form = ShipmentForm()

    lines = (
        request.form.getlist('product_id[]'),
        request.form.getlist('seller_id[]'),
        request.form.getlist('quantity[]'),
        request.form.getlist('price[]'),
    )

    shipment = {'title': form.title.data,
             'customer_id': form.customer_id.data,
             'shipping_dt': form.shipping_dt.data,
    }

    if form.validate_on_submit():
        shipmentServices.create_shipment_and_parse_line(
            shipment=shipment, lines=lines)
        #flash(f'People created for {form.firstname.data}!', 'success')
        return redirect('/shipments')

    customers = customerService.optim_get_all()

    return render_template('/shipments/create_shipment.html', title='Creation de livraison', form=form, customers=customers)


#####################################################################
#                                                                   #
#####################################################################
@shipment_page.route("/shipments/update/<int:shipment_id>", methods=['GET', 'POST'])
@login_required
def shipment_update(shipment_id):
    form = ShipmentForm()

    # lines = (
    #     request.form.getlist('product_id[]'),
    #     request.form.getlist('quantity[]'),
    #     request.form.getlist('price[]'),
    # )

    # if form.validate_on_submit():
    #     shipmentServices.update_shipment_and_parse_line(
    #         shipment_id=shipment_id, lines=lines)
    #     #flash(f'People created for {form.firstname.data}!', 'success')
    #     return redirect(f'/shipments/{shipment_id}')

    # shipment = shipmentServices.get_one(shipment_id)
    # str_lines = str(shipment['lines'])
    # str_lines = str_lines.replace("{", "\{").replace("}", "\}")

    # return render_template('/shipments/update_shipment.html', shipment=shipment, str_lines=str_lines, title='Mise à jour de commande', form=form)


#####################################################################
#                                                                   #
#####################################################################
@shipment_page.route("/shipments/<int:shipment_id>", methods=['GET', 'POST'])
@login_required
def shipment(shipment_id):
    shipment = shipmentServices.get_one(shipment_id)
    return render_template('/shipments/shipment.html', shipment=shipment)

#####################################################################
#                                                                   #
#####################################################################
@shipment_page.route("/shipments/<int:shipment_id>/shipping_dt", methods=['GET', 'POST'])
@login_required
def display_update_shipment_time(shipment_id):

    shipment = shipmentServices.get_one(shipment_id)
    form = ShippingDtForm()

    if form.validate_on_submit():
        shipmentServices.update_shipping_dt(
            shipment, shipping_dt=form.shipping_dt.data)
        return redirect('/shipments')

    return render_template('/shipments/update_shipping_dt.html', shipment=shipment, title='Mise a jour du jour de la commande', form=form)

#####################################################################
#                                                                   #
#####################################################################
@shipment_page.route("/shipments/<int:shipment_id>/cancel", methods=['GET', 'POST'])
@login_required
def display_update_shipment_annulation(shipment_id):
    shipmentServices.update_shipment_status(shipment_id, ShipmentStatus_Enum.ANNULEE.value)
    return redirect('/shipments')

#####################################################################
#                                                                   #
#####################################################################

@shipment_page.route("/shipments/<int:shipment_id>/created", methods=['GET', 'POST'])
@login_required
def display_update_shipment_created(shipment_id):
    shipmentServices.update_shipment_status(shipment_id, ShipmentStatus_Enum.CREE.value)
    return redirect('/shipments')

#####################################################################
#                                                                   #
#####################################################################

@shipment_page.route("/shipments/<int:shipment_id>/shipped/<string:status>", methods=['GET', 'POST'])
@login_required
def update_shipment_shipped(shipment_id, status):
    if status == 'NON':
        shipmentServices.update_shipment_shipping_status(shipment_id, ShippingStatus_Enum.NON.value)
    else:
        shipmentServices.update_shipment_shipping_status(shipment_id, ShippingStatus_Enum.OUI.value)
    return redirect('/shipments')

#####################################################################
#                                                                   #
#####################################################################


@shipment_page.route("/shipments/<int:shipment_id>/paid/<string:status>", methods=['GET', 'POST'])
@login_required
def update_shipment_paid(shipment_id, status):
    if status == 'NON':
        shipmentServices.update_shipment_payment_status(
            shipment_id, PaymentStatus_Enum.NON.value)
    else:
        shipmentServices.update_shipment_payment_status(
            shipment_id, PaymentStatus_Enum.OUI.value)
    return redirect('/shipments')


#####################################################################
#                                                                   #
#####################################################################
@shipment_page.route("/shipments/delete/<int:shipment_id>")
@login_required
def display_delete_shipment(shipment_id):
    shipment = shipmentServices.get_one(shipment_id)
    return render_template('/shipments/delete_shipment.html', shipment=shipment, title='Suppression de commande')

#####################################################################
#                                                                   #
#####################################################################
@shipment_page.route("/shipments/<int:shipment_id>", methods=['DELETE'])
@login_required
def delete_shipment(shipment_id):
    shipmentServices.delete_shipment(shipment_id)
    return jsonify(success=True)

#####################################################################
#                                                                   #
#####################################################################
@shipment_page.route('/api/shipments/')
@login_required
def api_shipments():
    return jsonify({'shipments': shipmentServices.get_all()})

#####################################################################
#                                                                   #
#####################################################################
@shipment_page.route('/api/shipments/subscriptions/<int:subscription_id>')
@login_required
def api_shipments_by_subscription(subscription_id):
    return jsonify({'shipments': shipmentServices.get_all_by_subscription(subscription_id)})

#####################################################################
#                                                                   #
#####################################################################
@shipment_page.route('/api/shipments/customers/<int:customer_id>')
@login_required
def api_shipments_by_customer(customer_id):
    return jsonify({'shipments': shipmentServices.get_all_by_customer(customer_id)})

#####################################################################
#                                                                   #
#####################################################################
@shipment_page.route('/api/shipments/sellers/<int:seller_id>')
@login_required
def api_shipments_by_seller(seller_id):
    return jsonify({'shipments': shipmentServices.get_all_by_seller(seller_id)})


#####################################################################
#                                                                   #
#####################################################################
@shipment_page.route('/api/shipments/period/<string:period>/customers/<int:customer_id>')
@login_required
def api_day_shipments(period, customer_id):
    return jsonify({'shipments': shipmentServices.get_some(period=period, customer_id=customer_id)})

