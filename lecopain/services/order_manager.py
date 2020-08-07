from datetime import datetime, date, timedelta

from lecopain.app import app, db
from lecopain.services.business_service import BusinessService
from lecopain.services.item_service import ItemService
from lecopain.dao.models import Line, Product, Seller, Customer, Order, OrderStatus_Enum, ShipmentStatus_Enum
from lecopain.helpers.date_utils import dates_range, Period_Enum
from lecopain.dao.order_dao import OrderDao
from lecopain.dao.subscription_dao import SubscriptionDao
from lecopain.dao.product_dao import ProductDao
from lecopain.dao.shipment_dao import ShipmentDao

import json
from sqlalchemy import extract, Date, cast

class OrderManager():

    businessService = BusinessService()
    itemService = ItemService()

    def parse_lines(self, lines):
        headers = ('product_id', 'quantity', 'price' )
        items = [{} for i in range(len(lines[0]))]
        for x, i in enumerate(lines):
            for _x, _i in enumerate(i):
                items[_x][headers[x]] = _i
        return items

    def create_by_shipment(self, shipment, lines, seller_id):
        created_order = OrderDao.create_by_shipment(shipment, lines, seller_id)
        shipment.active_order(created_order)

    def update_by_shipment(self, shipment, lines, seller_id):
        order = OrderDao.find_by_shipment_and_seller_id(shipment.id, seller_id)

        if order is None:
            self.create_by_shipment(shipment, lines, seller_id)
        else:
            shipment.remove_order(order)
            OrderDao.remove_all_lines(order)
            OrderDao.add_lines(order, lines)
            order.updated_at = datetime.now()
            OrderDao.update_db(order)
            shipment.add_order(order)


    def create_order_and_parse_line(self, order, lines):
        parsed_lines = self.parse_lines(lines)
        created_order = OrderDao.create_order(order, parsed_lines)
        db.session.commit()

    def delete_order(self, order_id):
        order = OrderDao.get_one(order_id)
        if order.status != OrderStatus_Enum.ANNULEE.value and \
            order.shipment_id is not None:
            self.remove_order_to_shipment(order)

        if order.status != OrderStatus_Enum.ANNULEE.value and \
            order.shipment_id is not None and order.shipment.subscription_id is not None:
            self.remove_order_to_subscription(order)

        OrderDao.delete(order_id)
        OrderDao.update_db(order)


    # def update_order_and_parse_line(self, order_id, lines):
    #     parsed_lines = self.parse_lines(lines)
    #     order = OrderDao.get_one(order_id)
    #     if order.subscription_id is not None:
    #         self.items_remove_subscription(order)
    #     OrderDao.remove_all_lines(order)
    #     order.shipping_price = 0.0
    #     order.nb_products = 0
    #     order.shipping_rules = ''
    #     OrderDao.add_lines(order, parsed_lines)
    #     order.category = order.products[0].category
    #     order.updated_at = datetime.now()
    #     OrderDao.update_db(order)
        
    #     order.shipment = order.products[0].category
    #     order.shipment.shipping_price, ordershipment.shipping_rules = self.businessService.apply_rules_for_shipment(
    #         order.shipment)
    #     ShipmentDao.update_db(order.shipment)
        
    #     if order.subscription_id is not None:
    #         self.items_add_subscription(order)
    #     db.session.commit()

    def remove_order_to_shipment(self, order):
        shipment = ShipmentDao.get_one(order.shipment_id)
        shipment.remove_order(order)
        self.decrement_to_shipment(order)
    
    def cancel_order_to_shipment(self, order):
        shipment = ShipmentDao.get_one(order.shipment_id)
        shipment.cancel_order(order)
        self.decrement_to_shipment(order)
        
    def add_order_to_shipment(self, order):
        shipment = ShipmentDao.get_one(order.shipment_id)
        shipment.add_order(order)
        self.increment_to_shipment(order)
    
    def active_order_to_shipment(self, order):
        shipment = ShipmentDao.get_one(order.shipment_id)
        shipment.active_order(order)
        self.increment_to_shipment(order)
        
        
    def decrement_to_shipment(self, order):
        shipment = order.shipment
        
        if(shipment.shipping_price is not None):
            old_shipping_price = shipment.shipping_price
        else:
            old_shipping_price = 0.0
        
        shipment.shipping_price, shipment.shipping_rules = self.businessService.apply_rules_for_shipment(shipment)
        diff_shipping_price = old_shipping_price - float(shipment.shipping_price)

        if order.shipment.subscription != None:
            order.shipment.subscription.shipping_price = order.shipment.subscription.shipping_price - diff_shipping_price
        
        order.shipment.updated_at = datetime.now()
        ShipmentDao.update_db(order.shipment)
        
    def increment_to_shipment(self, order):
        shipment = order.shipment
        
        old_shipping_price = shipment.shipping_price
        shipment.shipping_price, shipment.shipping_rules = self.businessService.apply_rules_for_shipment(
            shipment)
        diff_shipping_price = old_shipping_price - float(shipment.shipping_price)
        
        if order.shipment.subscription != None:
            order.shipment.subscription.shipping_price = order.shipment.subscription.shipping_price + diff_shipping_price
        
        order.shipment.updated_at = datetime.now()
        ShipmentDao.update_db(order.shipment)

    def remove_lines_to_order(self, order):
        order.remove_lines()

    def remove_order_to_subscription(self, order):
        order.shipment.subscription.remove_order(order)


    def remove_order_subscriptions(self, order):
        subscription = SubscriptionDao.get_one(order.subscription_id)
        itemService = ItemService()
        itemService.decrement_subscription_nb_order(subscription) \
            .remove_order_subscription_nb_products(subscription, order.nb_products) \
            .remove_order_subscription_shipping_price(subscription, order.shipping_price) \
            .remove_order_subscription_price(subscription, order.price)
        SubscriptionDao.update_db(subscription, itemService.items)

    def items_remove_subscription(self, order):
        subscription = SubscriptionDao.get_one(order.subscription_id)
        itemService = ItemService()
        itemService.remove_order_subscription_nb_products(subscription, order.nb_products) \
            .remove_order_subscription_shipping_price(subscription, order.shipping_price) \
            .remove_order_subscription_price(subscription, order.price)
        SubscriptionDao.update_db(subscription, itemService.items)

    def items_add_subscription(self, order):
        subscription = SubscriptionDao.get_one(order.subscription_id)
        itemService = ItemService()
        itemService.add_order_subscription_nb_products(subscription, order.nb_products) \
            .add_shipment_subscription_shipping_price(subscription, order.shipment.shipping_price) \
            .add_order_subscription_price(subscription, order.price)
        SubscriptionDao.update_db(subscription, itemService.items)

    # @
    #
    def update_order_status(self, order_id, order_status):
        order = OrderDao.get_one(order_id)
        if order_status == OrderStatus_Enum.ANNULEE.value:
            self.cancel_order(order)

        if order_status == OrderStatus_Enum.CREE.value:
            self.active_order(order)

    def cancel_order(self, order):
        OrderDao.update_status(order.id, OrderStatus_Enum.ANNULEE.value)
        if order.shipment_id is not None:
            self.cancel_order_to_shipment(order)

        if order.shipment.subscription_id is not None:
            self.remove_order_to_subscription(order)
        order.shipment.updated_at = datetime.now()
        ShipmentDao.update_db(order.shipment)

    def active_order(self, order):
        OrderDao.update_status(order.id, OrderStatus_Enum.CREE.value)
        if order.shipment_id is not None:
            self.active_order_to_shipment(order)

        if order.shipment.subscription_id is not None:
            self.add_order_to_subscription(order)
        order.shipment.updated_at = datetime.now()
        ShipmentDao.update_db(order.shipment)

    # @
    #
    def update_order_shipping_status(self, order_id, order_status):
        OrderDao.update_shipping_status(order_id, order_status)

    # @
    #
    def update_order_payment_status(self, order_id, order_status):
        OrderDao.update_payment_status(order_id, order_status)

    # @
    #
    def get_in_progess_orders_counter(self):
        return Order.query.filter(Order.status == OrderStatus_Enum.CREE.value).count()

    # @
    #
    def get_latest_orders_counter(self):
        date_since_2_days = date.today() - timedelta(days=2)
        return Order.query.filter(Order.created_at > date_since_2_days).count()

    def get_all(self):
        return OrderDao.read_all()

    def get_all_by_subscription(self, subscription_id):
        return OrderDao.read_by_subscription(subscription_id)

    def get_all_by_customer(self, customer_id):
        return OrderDao.read_by_customer(customer_id)
    
    def get_all_by_seller(self, seller_id):
        return OrderDao.read_by_seller(seller_id)
    
    def get_all_by_seller_pagination(self, seller_id, page=1, per_page=10):
        return OrderDao.read_by_seller_pagination(seller_id, page=page, per_page=per_page)

    def get_all_by_seller_period(self, seller_id, start, end):
        return OrderDao.read_some_seller(seller_id=seller_id, start=start, end=end)
    
    def get_all_by_seller_period_valid(self, seller_id, start, end):
        return OrderDao.read_some_seller_valid(seller_id=seller_id, start=start, end=end)
    
    def get_all_by_seller_customer_period_valid(self, seller_id, customer_id, start, end):
        return OrderDao.read_some_seller_customer_valid(seller_id=seller_id, customer_id=customer_id, start=start, end=end)

    def get_some_by_customer(self,  customer_id=0, period=Period_Enum.ALL.value):
        start,end = dates_range(period)
        return OrderDao.read_some(customer_id=customer_id, start=start, end=end)
    
    def get_some_by_seller(self,  seller_id=0, period=Period_Enum.ALL.value):
        start,end = dates_range(period)
        return OrderDao.read_some_seller(seller_id=seller_id, start=start, end=end)
    
    def get_some_by_seller_valid(self,  seller_id=0, period=Period_Enum.ALL.value):
        start,end = dates_range(period)
        return OrderDao.read_some_seller_valid(seller_id=seller_id, start=start, end=end)

    def get_one(self,  order_id):
        return OrderDao.read_one(order_id)

    def get_order_status(self):
        return list(map(lambda c: c.value, OrderStatus_Enum))

    def update_shipping_dt(self, order, shipping_dt):
        OrderDao.update_shipping_dt(order['id'], shipping_dt)

    def find(self, products, short_name):
        for product in products: 
            if product['short_name'] == short_name: 
                return product
        return None

    def extract_products_from_orders(self, orders, dt=None):
        products = []
        product = None
        for order in orders:
            shipping_day = order['shipping_dt'].day
            if dt is None or int(shipping_day) == dt.day:
                for line in order['lines']:
                    short_name = line['product_short_name']
                    quantity  = line['quantity']
                    product = self.find(products, short_name) 
                    if product != None:
                        #line_tmp = [d for d in order['lines'] if d['line']['product_short_name'] == short_name]
                        product['quantity'] = product['quantity'] + int(line['quantity'])
                    else :
                        products.append({'short_name':line['product_short_name'], 'quantity':int(line['quantity'])})
        return products
            

            



