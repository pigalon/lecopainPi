from lecopain.app import db

from lecopain.dao.models import (
    Order, OrderSchema
)

class OrderDao:

    @staticmethod
    def read_all():

        # Create the list of people from our data

        all_orders = Order.query \
            .order_by(Order.shipping_dt.desc()) \
            .all()

        # Serialize the data for the response
        order_schema = OrderSchema(many=True)
        return order_schema.dump(all_orders)

    @staticmethod
    def read_one(id):

        # Create the list of people from our data
        order = Order.query.get_or_404(id)

        # Serialize the data for the response
        order_schema = OrderSchema(many=False)
        return order_schema.dump(order)
    
    @staticmethod
    def read_some(customer_id, start, end):
        
        all_orders = Order.query
        
        if(start != 0 ):
            all_orders = all_orders.filter(
                Order.shipping_dt >= start).filter(
                Order.shipping_dt <= end)
        
        if customer_id != 0:
            all_orders = all_orders.filter(
                Order.customer_id == customer_id)

        all_orders = all_orders.order_by(Order.shipping_dt.desc()) \
        .all()

        # Serialize the data for the response
        order_schema = OrderSchema(many=True)
        return order_schema.dump(all_orders)
