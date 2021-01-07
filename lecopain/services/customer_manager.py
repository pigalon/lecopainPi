from lecopain.app import app, db
from lecopain.dao.models import Customer, Order
from lecopain.dao.customer_dao import CustomerDao
from lecopain.dao.shipment_dao import ShipmentDao

class Report():
  shipments_count  = 0
  effective_count  = 0
  canceled_count   = 0
  paid_count       = 0
  in_sub_count     = 0
  out_sub_count    = 0
  shipments_sum    = 0

class CustomerManager():

  def get_last_order(self, customer):
    newer_order = None
    for order in customer.orders:
        if(newer_order == None):
            print("newer from null")
            newer_order = order
        elif (order.shipping_dt > newer_order.shipping_dt):
            newer_order = order
            print("newer from other")
    return newer_order

  def get_all(self):
    return CustomerDao.read_all()

  def optim_get_all(self):
    return CustomerDao.optim_read_all()
  
  def read_one(self, id):
    return CustomerDao.read_one(id)

  def get_one(self, id):
    return CustomerDao.get_one(id)

  def get_all_cities(self):
    return CustomerDao.get_all_cities()

  def get_all_by_city(self, city):
    return CustomerDao.read_all_by_cities(city)

  def get_all_by_city_pagination(self, city, page=1, per_page=10):
    return CustomerDao.read_all_by_cities_pagination(city, page, per_page)
  
  def add_customer_form(self, form):
    customer = Customer(firstname=form.firstname.data,
                        lastname=form.lastname.data, email=form.email.data)
    customer.address = form.address.data
    customer.cp = form.cp.data
    customer.city = form.city.data
    CustomerDao.add(customer)
      
  def update_customer_form(self, customer_id, form):
    customer = CustomerDao.get_one(customer_id)

    customer.firstname = form.firstname.data
    customer.lastname = form.lastname.data
    customer.email = form.email.data
    customer.address = form.address.data
    customer.cp = form.cp.data
    customer.city = form.city.data
    
    CustomerDao.update()

  def delete(self, id):
    customer = CustomerDao.get_one(id)
    CustomerDao.delete(customer)
    
  def getAllReports(self, id):
    reports = {'current' : Report(), 'last' : Report(), 'global' : Report()}
    #get_current_month() and get_current_year
    #get_last_month() and get_last_year
    reports['global'].shipments_count =  ShipmentDao.count_by_customer(id)
    reports['global'].shipments_sum =  ShipmentDao.sum_by_customer(id)
    reports['global'].canceled_count = ShipmentDao.count_canceled_by_customer(id)
    reports['global'].paid_count = ShipmentDao.count_paid_by_customer(id)
    reports['global'].effective_count = ShipmentDao.count_effective_by_customer(id)
    reports['global'].in_sub_count = ShipmentDao.count_in_sub_by_customer(id)
    reports['global'].out_sub_count = ShipmentDao.count_out_sub_by_customer(id)
    
    return reports
