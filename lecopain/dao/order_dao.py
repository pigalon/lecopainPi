from lecopain.app import db

from lecopain.dao.models import (
    Order, Line, Seller, Customer, OrderSchema, CompleteOrderSchema
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
    def read_by_subscription(subscription_id):
        all_orders = Order.query \
            .filter(Order.subscription_id == subscription_id) \
            .order_by(Order.shipping_dt.desc()) \
            .all()

        # Serialize the data for the response
        order_schema = OrderSchema(many=True)
        return order_schema.dump(all_orders)

    @staticmethod
    def read_by_customer(customer_id):
        all_orders = Order.query \
            .filter(Order.customer_id == customer_id) \
            .order_by(Order.shipping_dt.desc()) \
            .all()

        # Serialize the data for the response
        order_schema = OrderSchema(many=True)
        return order_schema.dump(all_orders)

    @staticmethod
    def read_by_seller(seller_id):
        all_orders = Order.query \
            .filter(Order.seller_id == seller_id) \
            .order_by(Order.shipping_dt.desc()) \
            .all()

        # Serialize the data for the response
        order_schema = OrderSchema(many=True)
        return order_schema.dump(all_orders)

    @staticmethod
    def get_one(id):
        return Order.query.get_or_404(id)


    @staticmethod
    def read_one(id):

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
    def read_some_seller(seller_id, start, end):

        all_orders = Order.query

        if(start != 0 ):
            all_orders = all_orders.filter(
                Order.shipping_dt >= start).filter(
                Order.shipping_dt <= end)

        if seller_id != 0:
            all_orders = all_orders.filter(
                Order.seller_id == seller_id)

        all_orders = all_orders.order_by(Order.shipping_dt.desc()) \
        .all()

        # Serialize the data for the response
        order_schema = CompleteOrderSchema(many=True)
        return order_schema.dump(all_orders)

    @staticmethod
    def add(order):
        customer = Customer.query.get_or_404(int(order.get('customer_id')))
        seller = Seller.query.get_or_404(int(order.get('seller_id')))
        # TODO
        ## get Customer address =| set order address

        created_order = Order(title=order.get('title'),
            status=order.get('status'),
            customer_id=order.get('customer_id'),
            seller_id=order.get('seller_id'),
            shipping_dt=order.get('shipping_dt'),
            category=order.get('category'),
            shipping_address = customer.address,
            shipping_cp=customer.cp,
            shipping_city=customer.city)
        db.session.add(created_order)
        customer.nb_orders = customer.nb_orders + 1
        seller.nb_orders = seller.nb_orders + 1
        return created_order

    @staticmethod
    def add_lines(order, lines):
        nb_products = 0
        total_price = 0.0
        for line in lines :
            product_id, qty, price = list(line.values())
            nb_products = nb_products + int(qty)
            total_price = total_price + int(qty) * float(price)
            order.lines.append(Line(
                order=order, product_id=product_id, quantity=qty, price=float(price)))
        order.price = format(total_price, '.2f')
        order.nb_products = nb_products

    @staticmethod
    def update_shipping_dt(id, shipping_dt):
        order = order = Order.query.get_or_404(id)
        order.shipping_dt = shipping_dt
        db.session.commit()

    @staticmethod
    def update_status(id, status):
        order = order = Order.query.get_or_404(id)
        order.status = status
        db.session.commit()

    @staticmethod
    def update_shipping_status(id, status):
        order = order = Order.query.get_or_404(id)
        order.shipping_status = status
        db.session.commit()

    @staticmethod
    def update_payment_status(id, status):
        order = order = Order.query.get_or_404(id)
        order.payment_status = status
        db.session.commit()

    @staticmethod
    def delete(id):
        order = order = Order.query.get_or_404(id)
        customer = Customer.query.get_or_404(order.customer.id)
        db.session.delete(order)
        customer.nb_subscriptions = customer.nb_orders - 1
        db.session.commit()

    # @
    #
    @staticmethod
    def create_order(order, lines):
        created_order = OrderDao.add(order)
        db.session.flush()
        OrderDao.add_lines(created_order, lines)
        db.session.commit()
        return created_order
    
    # @
    #
    @staticmethod
    def remove_all_lines(order):
        for line in order.lines :
            db.session.delete(line)
        db.session.commit()

    @staticmethod
    def update_db(order):
        db.session.commit()
