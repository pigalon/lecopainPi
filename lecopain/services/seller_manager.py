from lecopain.app import app, db
from lecopain.dao.models import CustomerOrder, Seller, SellerOrder


class SellerManager():

    def get_last_order(self, seller):

        newer_order = None
        orders = CustomerOrder.query.filter(
            SellerOrder.seller_id == seller.id).all()
        for order in orders:
            if(newer_order == None):
                print("newer from null")
                newer_order = order
            elif (order.shipping_dt > newer_order.shipping_dt):
                newer_order = order
                print("newer from other")
        return newer_order
