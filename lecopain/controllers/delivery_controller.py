from lecopain.models import Product, DeliveryStatus, Delivery, Vendor
from lecopain import app, db
from lecopain.form import DeliveryForm
from lecopain.services.delivery_manager import DeliveryManager
from lecopain.dao.customer import Customer, CustomerOrder

from sqlalchemy import extract
from datetime import datetime
from calendar import Calendar
from datetime import date

from flask import Blueprint, render_template, redirect, url_for, Flask, request, jsonify

app = Flask(__name__, instance_relative_config=True)

delivery_page = Blueprint('delivery_page', __name__,
                        template_folder='../templates')

delivery_services = DeliveryManager()


#####################################################################
#                                                                   #
#####################################################################
@delivery_page.route("/deliveries/<int:customer_id>", methods=['GET', 'POST'])
def deliveries(customer_id):
    print(" deliveries ")
  
    year = date.today().year
    month = date.today().month  
    if(year == 0) :
        year = datetime.now().year
    
    if(month == 0) :
        month = datetime.now().month
        
    if(customer_id == 0 or customer_id == None):
        deliveries = Delivery.query.filter(extract('year', Delivery.delivery_dt) == year).filter(extract('month', Delivery.delivery_dt) == month).all()
        customer = Customer()
        customer.id = 0
    else :    
        deliveries = Delivery.query.filter(Delivery.customer_id == customer_id).filter(extract('year', Delivery.delivery_dt) == year).filter(extract('month', Delivery.delivery_dt) == month).all()
        customer = Customer.query.get_or_404(customer_id)
    
    customers = Customer.query.all()
    #deliveries = Delivery.query.filter().order_by(Delivery.delivery_dt.desc()).all()
    map_deliveries = {}
    for delivery in deliveries :
        map_deliveries[delivery.delivery_dt.day * delivery.delivery_dt.month] = delivery.customer_order_id
    
    print(" deliveries 2 - size : " + str(len(map_deliveries)))
    for key in map_deliveries :
        print(str(key))
    
    map = delivery_services.get_maps_from_deliveries(deliveries)
    print(" deliveries fin")
    
    cal = Calendar(0)


    cal_list = [
        cal.monthdatescalendar(year, month)
        for i in range(1)
    ]
    for i in range (0, len(cal_list)):
        print(str(cal_list[i]))
    
    return render_template('/deliveries/deliveries.html', customer=customer, title="", map=map, year=year, cal=cal_list, month_param=month, map_deliveries=map_deliveries, customers=customers)

#####################################################################
#                                                                   #
#####################################################################
@delivery_page.route("/deliveries/year/<int:year_number>/month/<int:month_number>", methods=['GET', 'POST'])
def deliveries_of_month(year_number, month_number):
    print(str(datetime.today().month) + " - " + str(datetime.today().day))
    
    if(year_number == 0) :
        year_number = datetime.now().year
    
    if(month_number == 0) :
        month_number = datetime.now().month

    deliveries = Delivery.query.filter(extract('year', Delivery.delivery_dt) == year_number).filter(extract('month', Delivery.delivery_dt) == month_number).all()
    #map = order_services.get_maps_from_orders(orders)
   
    return render_template('/deliveries/deliveries.html', deliveries=deliveries, title="livraisons du mois")

#####################################################################
#                                                                   #
#####################################################################
@delivery_page.route("/deliveries/year/<int:year_number>/month/<int:month_number>/day/<int:day_number>", methods=['GET', 'POST'])
def deliveries_of_day(year_number, month_number, day_number):
    print(str(datetime.today().month) + " - " + str(datetime.today().day))
    if(year_number == 0) :
        year_number = datetime.now().year
    
    if(month_number == 0) :
        month_number = datetime.now().month
    
    if(day_number == 0) :
        day_number = datetime.now().month

    deliveries = Delivery.query.filter(extract('year', Delivery.delivery_dt) == year_number).filter(extract('month', Delivery.delivery_dt) == month_number).filter(extract('day', Delivery.delivery_dt) == day_number).all()
    
    map = delivery_services.get_maps_from_orders(deliveries)

    return render_template('/orders/year/'+year_number+'/month/'+month_number+'/day/'+day_number+'.html', deliveries=deliveries, title="Livraisons du jour")


#####################################################################
#                                                                   #
#####################################################################
@delivery_page.route("/deliveries/new", methods=['GET', 'POST'])
def delivery_create():
    form = DeliveryForm()

    vendors = Vendor.query.all()
    
    #tmp_order = request.form.getlist('orders')


    if form.validate_on_submit():

        #delivery_dt=datetime.strptime('YYYY-MM-DD HH:mm:ss', form.delivery_dt.data)
        delivery = Delivery(reference=form.reference.data, status=form.status.data, customer_id=int(form.customer_id.data), delivery_dt=form.delivery_dt.data)

        db.session.add(delivery)
        db.session.commit()

        #flash(f'People created for {form.firstname.data}!', 'success')
        return redirect(url_for('delivery_page.deliveries'))
    else:
        customers = Customer.query.all()
        products = Product.query.all()
    #else:
    #    flash(f'Failed!', 'danger')
    deliveryStatusList = _get_delivery_status()

    return render_template('/deliveries/create_delivery.html', title='Creation de livraison', form=form, customers=customers, vendors=vendors, deliveryStatusList=deliveryStatusList)

#####################################################################
#                                                                   #
#####################################################################
@delivery_page.route("/deliveries/<int:delivery_id>", methods=['GET', 'POST'])
def delivery(delivery_id):
    delivery = Delivery.query.get_or_404(delivery_id)
    return render_template('/deliveries/delivery.html', delivery=delivery)

#####################################################################
#                                                                   #
#####################################################################
@delivery_page.route("/deliveries/update/<int:delivery_id>", methods=['GET', 'POST'])
def display_update_delivery(delivery_id):
    delivery = Delivery.query.get_or_404(delivery_id)
    form = DeliveryForm()

    customers = Customer.query.all()
    products = Product.query.all()
    
    #order_product_selection = Delivery_product.query.filter(Delivery_product.delivery_id == order.id).all()

    if form.validate_on_submit():
        print('update form validate : ' + str(delivery.id))

        #delivery_dt=datetime.strptime('YYYY-MM-DD HH:mm:ss', form.delivery_dt.data)
        deliveryForm = Delivery(reference=form.reference.data, status=form.status.data, customer_id=int(form.customer_id.data), delivery_dt=form.delivery_dt.data)
        delivery.reference = deliveryForm.reference
        delivery.status = deliveryForm.status
        delivery.customer_id = deliveryForm.customer_id
        delivery.delivery_dt = deliveryForm.delivery_dt
        #products = {}

        #Delivery_product.query.filter(Delivery_product.order_id == order.id).delete()

        #tmp_products = request.form.getlist('products')
        #tmp_quantities = request.form.getlist('quantities')

        #for i in range(0,len(tmp_products)): 
        #    product = Product.query.get(tmp_products[i])
        #    order.selected_products.append(product)

        #db.session.add(order)
        db.session.commit()

    
        
        #flash(f'People created for {form.firstname.data}!', 'success')
        return redirect(url_for('delivery_page.deliveries'))
    else:
        form.customer_order_id.data = delivery.customer_order_id
        form.delivery_dt.data = delivery.delivery_dt
        form.status.data = delivery.status
        form.reference.data = delivery.reference
        

    orderStatusList = _get_delivery_status()
    return render_template('/deliveries/update_delivery.html', delivery=delivery, title='Mise a jour de livraison', form=form, customers=customers, products=products,  deliveryStatusList=orderStatusList)

#####################################################################
#                                                                   #
#####################################################################
@delivery_page.route("/deliveries/delete/<int:delivery_id>")
def display_delete_delivery(delivery_id):
    delivery = Delivery.query.get_or_404(delivery_id)
    return render_template('/deliveries/delete_delivery.html', delivery=delivery, title='Suppression de livraison')

#####################################################################
#                                                                   #
#####################################################################
@delivery_page.route("/deliveries/<int:delivery_id>", methods=['DELETE'])
def delete_delivery(delivery_id):
    delivery = Delivery.query.get_or_404(delivery_id)
    db.session.delete(delivery)
    db.session.commit()
    return jsonify({})
#####################################################################
#                                                                   #
#####################################################################
@delivery_page.route('/_get_delivery_status/')
def _get_delivery_status():
    deliveriesStatusList = [(row.name) for row in DeliveryStatus.query.all()]
    return deliveriesStatusList

class Event():
    title = ''
    description = ''
    start='2019-05-05'
    color='#FFBF00'

    def __init__(self, title, description, start, color): 
        self.title = title
        self.description = description
        self.start = start
        self.color = color
    def to_dict(self)           : 
        return {
            'title'             : self.title,
            'description'       : self.description,
            'start'            : self.start,
            'color'            : self.color
        }

#####################################################################
#                                                                   #
#####################################################################
@delivery_page.route('/_getjs_delivery_event/customer/<int:customer_id>')
def _getjs_delivery_event(customer_id):
    events=[]
    
    #if(year_number == 0) :
    year_number = datetime.now().year
    
    #if(month_number == 0) :
    month_number = datetime.now().month
    
    #if(day_number == 0) :
    day_number = datetime.now().month
    
    orders =  CustomerOrder.query.filter(CustomerOrder.customer_id == customer_id).filter(extract('month', Delivery.delivery_dt) == month_number).all()
    
    

    #deliveries = Delivery.query.filter(extract('year', Delivery.delivery_dt) == year_number).filter(extract('month', Delivery.delivery_dt) == month_number).filter(extract('day', Delivery.delivery_dt) == day_number).all()
    
    
    #for devlivery 
    event1 = Event(title='All day event', description='', start='2019-05-05', color='#FFBF00')
    #events = "[{'title': 'All Day Event','start': '2019-05-05','color': '}]"
    events.append(event1.to_dict())
    #return jsonify([(row.to_dict()) for event in events
    
    return jsonify({'events': events})
