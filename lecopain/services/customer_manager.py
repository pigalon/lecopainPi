from lecopain.app import app, db
from lecopain.dao.models import Customer, Order
from lecopain.dao.customer_dao import CustomerDao


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

