from lecopain.app import db

from lecopain.dao.models import (
    Order, Line, Customer, OrderSchema, CompleteOrderSchema
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
        customer = Customer.query.get_or_404(int(order.get('customer_id')))
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
    def update(order):
        created_order = Order(title=order.get('title'),
                              status=order.get('status'),
                              customer_id=order.get('customer_id'),
                              seller_id=order.get('seller_id'),
                              shipping_dt=order.get('shipping_dt'))
        db.session.add(created_order)
        return created_order
    
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
        db.session.delete(order)
        db.session.commit()

    # @
    #
    @staticmethod
    def create_order(order, lines):
        # order = OrderDao.set_order_category(order, lines)
        created_order = OrderDao.add(order)
        db.session.flush()
        OrderDao.add_lines(created_order, lines)
        db.session.commit()
        return created_order

    @staticmethod
    def update_db(order):
        db.session.commit()
    
    # @
    #
    @staticmethod
    def generate_order(order_dict, lines):
        Order
        order = OrderDao.set_order_category(order, lines)
        created_order = OrderDao.add(order)
        db.session.flush()
        OrderDao.add_lines(created_order, lines)
        created_order.shipping_price, created_order.shipping_rules = self.businessService.apply_rules(
            created_order)
        db.session.commit()
