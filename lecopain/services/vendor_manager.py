from lecopain import app, db
from lecopain.models import Vendor, Order

class VendorManager():

    def get_last_order(self, vendor) :
        
        newer_order = None
        orders = Order.query.filter(Order.vendor_id == vendor.id).all()
        for order in orders :
            if(newer_order == None) :
                print("newer from null")
                newer_order = order
            elif (order.order_dt > newer_order.order_dt) :
                newer_order = order
                print("newer from other")
        return newer_order