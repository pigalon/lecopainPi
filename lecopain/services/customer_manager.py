from lecopain import app, db
from lecopain.models import Customer, Order

class CustomerManager():

    def get_last_order(self, customer) :
        newer_order = None
        for order in customer.orders :
            if(newer_order == None) :
                print("newer from null")
                newer_order = order
            elif (order.order_dt > newer_order.order_dt) :
                newer_order = order
                print("newer from other")
        return newer_order