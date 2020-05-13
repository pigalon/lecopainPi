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

    def get_one(self, id):
        return CustomerDao.read_one(id)
