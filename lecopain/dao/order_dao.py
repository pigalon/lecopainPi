from lecopain.app import db

from lecopain.dao.models import (
    Order, Line, OrderSchema, CompleteOrderSchema
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
        order_schema = CompleteOrderSchema(many=False)
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

    @staticmethod
    def add(order):
        created_order = Order(title=order.get('title'),
            status=order.get('status'),
            customer_id=order.get('customer_id'),
            seller_id=order.get('seller_id'),
            shipping_dt=order.get('shipping_dt'))
        db.session.add(created_order)
        return created_order

    @staticmethod
    def add_lines(order, lines):
        for line in lines :
            product_id, qty, price = list(line.values())
            print("price : " + price)
            order.lines.append(Line(
                order=order, product_id=product_id, quantity=qty, price=float(price)))
        db.session.commit()
