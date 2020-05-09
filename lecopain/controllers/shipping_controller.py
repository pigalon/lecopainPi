from lecopain.dao.models import Customer, Order, Product, ShippingStatus, Shipping, Seller
from lecopain.app import app, db
from lecopain.form import ShippingForm
from lecopain.services.shipping_manager import ShippingManager

from sqlalchemy import extract
from datetime import datetime
from calendar import Calendar
from datetime import date

from flask import Blueprint, render_template, redirect, url_for, Flask, request, jsonify
from flask_login import login_required

app = Flask(__name__, instance_relative_config=True)

shipping_page = Blueprint('shipping_page', __name__,
                          template_folder='../templates')

shipping_services = ShippingManager()


class Event():
    title = ''
    description = ''
    start = '2019-05-05'
    color = '#FFBF00'

    def __init__(self, title, description, start, color):
        self.title = title
        self.description = description
        self.start = start
        self.color = color

    def to_dict(self):
        return {
            'title': self.title,
            'description': self.description,
            'start': self.start,
            'color': self.color
        }


#####################################################################
#                                                                   #
#####################################################################
@shipping_page.route("/shippings", methods=['GET', 'POST'])
@login_required
def shippings():
    return shippings_customer(0)


@shipping_page.route("/shippings/customers/<int:customer_id>", methods=['GET', 'POST'])
@login_required
def shippings_customer(customer_id):

    year_number = datetime.now().year

    month_number = datetime.now().month

    if(customer_id == 0 or customer_id == None):
        shippings = Shipping.query.filter(extract('year', Shipping.shipping_dt) == year_number).filter(
            extract('month', Shipping.shipping_dt) == month_number).all()
        customer = Customer()
        customer.id = 0
    else:
        shippings = Shipping.query.filter(Shipping.customer_id == customer_id).filter(extract(
            'year', Shipping.shipping_dt) == year_number).filter(extract('month', Shipping.shipping_dt) == month_number).all()
        customer = Customer.query.get_or_404(customer_id)

    customers = Customer.query.all()
    #shippings = Shipping.query.filter().order_by(Shipping.shipping_dt.desc()).all()
    map_shippings = {}
    for shipping in shippings:
        map_shippings[shipping.shipping_dt.day *
                      shipping.shipping_dt.month] = shipping.order_id

    map = shipping_services.get_maps_from_shippings(shippings)

    cal = Calendar(0)
    cal_list = [
        cal.monthdatescalendar(year_number, month_number)
        for i in range(1)
    ]

    return render_template('/shippings/shippings.html', customer=customer, title="Les livraisons", map=map, year=year_number, cal=cal_list, month_param=month_number, map_shippings=map_shippings, customers=customers)

#####################################################################
#                                                                   #
#####################################################################
@shipping_page.route("/shippings/customers/<int:customer_id>/year/<int:year_number>/month/<int:month_number>", methods=['GET', 'POST'])
@login_required
def shippings_of_month(customer_id, year_number, month_number):

    if(year_number == 0):
        year_number = datetime.now().year

    if(month_number == 0):
        month_number = datetime.now().month

    if(customer_id == 0 or customer_id == None):
        shippings = Shipping.query.filter(extract('year', Shipping.shipping_dt) == year_number).filter(
            extract('month', Shipping.shipping_dt) == month_number).all()
        customer = Customer()
        customer.id = 0
    else:
        shippings = Shipping.query.filter(Shipping.customer_id == customer_id).filter(extract(
            'year', Shipping.shipping_dt) == year_number).filter(extract('month', Shipping.shipping_dt) == month_number).all()
        customer = Customer.query.get_or_404(customer_id)

    customers = Customer.query.all()

    map_shippings = {}
    for shipping in shippings:
        map_shippings[shipping.shipping_dt.day *
                      shipping.shipping_dt.month] = shipping.order_id

    map = shipping_services.get_maps_from_shippings(shippings)

    cal = Calendar(0)

    cal_list = [
        cal.monthdatescalendar(year_number, month_number)
        for i in range(1)
    ]

    return render_template('/shippings/shippings.html', customer=customer, title="", map=map, year=year_number, cal=cal_list, month_param=month_number, map_shippings=map_shippings, customers=customers)

#####################################################################
#                                                                   #
#####################################################################
@shipping_page.route("/shippings/year/<int:year_number>/month/<int:month_number>/day/<int:day_number>", methods=['GET', 'POST'])
@login_required
def shippings_of_day(year_number, month_number, day_number):

    if(year_number == 0):
        year_number = datetime.now().year

    if(month_number == 0):
        month_number = datetime.now().month

    if(day_number == 0):
        day_number = datetime.now().day

    shippings = Shipping.query.filter(extract('year', Shipping.shipping_dt) == year_number).filter(extract(
        'month', Shipping.shipping_dt) == month_number).filter(extract('day', Shipping.shipping_dt) == day_number).all()
    return render_template('/orders/customers/0'+str(year_number)+'/month/'+str(month_number)+'/day/'+str(day_number)+'.html', shippings=shippings, title="Livraisons du jour")


#####################################################################
#                                                                   #
#####################################################################
@shipping_page.route("/shippings/new", methods=['GET', 'POST'])
@login_required
def shipping_create():
    form = ShippingForm()

    sellers = Seller.query.all()

    #tmp_order = request.form.getlist('orders')

    if form.validate_on_submit():

        #shipping_dt=datetime.strptime('YYYY-MM-DD HH:mm:ss', form.shipping_dt.data)
        shipping = Shipping(reference=form.reference.data, status=form.status.data, customer_id=int(
            form.customer_id.data), shipping_dt=form.shipping_dt.data)

        db.session.add(shipping)
        db.session.commit()

        #flash(f'People created for {form.firstname.data}!', 'success')
        return redirect(url_for('shipping_page.shippings'))
    else:
        customers = Customer.query.all()
        products = Product.query.all()
    # else:
    #    flash(f'Failed!', 'danger')
    shippingStatusList = _get_shipping_status()

    return render_template('/shippings/create_shipping.html', title='Creation de livraison', form=form, customers=customers, sellers=sellers, shippingStatusList=shippingStatusList)

#####################################################################
#                                                                   #
#####################################################################
@shipping_page.route("/shippings/<int:shipping_id>", methods=['GET', 'POST'])
@login_required
def shipping(shipping_id):
    shipping = Shipping.query.get_or_404(shipping_id)
    return render_template('/shippings/shipping.html', shipping=shipping)

#####################################################################
#                                                                   #
#####################################################################
@shipping_page.route("/shippings/update/<int:shipping_id>", methods=['GET', 'POST'])
@login_required
def display_update_shipping(shipping_id):
    shipping = Shipping.query.get_or_404(shipping_id)
    form = ShippingForm()

    customers = Customer.query.all()
    products = Product.query.all()

    if form.validate_on_submit():

        shippingForm = Shipping(reference=form.reference.data, status=form.status.data, customer_id=int(
            form.customer_id.data), shipping_dt=form.shipping_dt.data)
        shipping.reference = shippingForm.reference
        shipping.status = shippingForm.status
        shipping.customer_id = shippingForm.customer_id
        shipping.shipping_dt = shippingForm.shipping_dt
        db.session.commit()
        return redirect(url_for('shipping_page.shippings'))
    else:
        form.order_id.data = shipping.order_id
        form.shipping_dt.data = shipping.shipping_dt
        form.status.data = shipping.status
        form.reference.data = shipping.reference

    orderStatusList = _get_shipping_status()
    return render_template('/shippings/update_shipping.html', shipping=shipping, title='Mise a jour de livraison', form=form, customers=customers, products=products,  shippingStatusList=orderStatusList)

#####################################################################
#                                                                   #
#####################################################################
@shipping_page.route("/shippings/delete/<int:shipping_id>")
@login_required
def display_delete_shipping(shipping_id):
    shipping = Shipping.query.get_or_404(shipping_id)
    return render_template('/shippings/delete_shipping.html', shipping=shipping, title='Suppression de livraison')

#####################################################################
#                                                                   #
#####################################################################
@shipping_page.route("/shippings/<int:shipping_id>", methods=['DELETE'])
@login_required
def delete_shipping(shipping_id):
    shipping = Shipping.query.get_or_404(shipping_id)
    db.session.delete(shipping)
    db.session.commit()
    return jsonify({})
#####################################################################
#                                                                   #
#####################################################################
@shipping_page.route('/_get_shipping_status/')
@login_required
def _get_shipping_status():
    shippingsStatusList = [(row.name) for row in ShippingStatus.query.all()]
    return shippingsStatusList

#####################################################################
#                                                                   #
#####################################################################
@shipping_page.route('/_getjs_shipping_event/customer/<int:customer_id>')
@login_required
def _getjs_shipping_event(customer_id):
    events = []

    # if(year_number == 0) :
    year_number = datetime.now().year

    # if(month_number == 0) :
    month_number = datetime.now().month

    # if(day_number == 0) :
    day_number = datetime.now().month

    orders = Order.query.filter(Order.customer_id == customer_id).filter(
        extract('month', Shipping.shipping_dt) == month_number).all()

    #shippings = Shipping.query.filter(extract('year', Shipping.shipping_dt) == year_number).filter(extract('month', Shipping.shipping_dt) == month_number).filter(extract('day', Shipping.shipping_dt) == day_number).all()

    # for devlivery
    event1 = Event(title='All day event', description='',
                   start='2019-05-05', color='#FFBF00')
    #events = "[{'title': 'All Day Event','start': '2019-05-05','color': '}]"
    events.append(event1.to_dict())
    # return jsonify([(row.to_dict()) for event in events

    return jsonify({'events': events})
