from datetime import datetime, date, timedelta

from lecopain.app import app, db
from lecopain.dto.BoughtProduct import BoughtProduct
from lecopain.dao.models import Line, Product, Seller, Customer, Order, OrderStatus_Enum
from lecopain.helpers.date_utils import dates_range, Period_Enum
from lecopain.dao.order_dao import OrderDao
import json
from sqlalchemy import extract, Date, cast



class OrderManager():


    # @
    #
    def create_order(self, order, tmp_products, tmp_quantities, tmp_prices):
        order.created_at = datetime.now()

        lines = []
        for i in range(len(tmp_products)):
            product = Product.query.get_or_404(tmp_products[i])
            quantity = tmp_quantities[i]
            price = tmp_prices[i]
            lines.append((product, quantity, price))
        return order.add_products(lines)

    # @
    #
    def update_order(self, order, products, quantities, prices):
        # TODO update date instead
        #order.created_at = datetime.now()
        self.delete_every_order_dependencies(order)
        self.create_order(order, products, quantities, prices)
        # order = self.create_product_purchases(
        #    order, products, quantities, prices)
        # db.session.commit()

    # @
    #

    def create_product_purchases(self, order, tmp_products, tmp_quantities, tmp_prices):
        order = self.create_products_for_specific_order(
            order=order, tmp_products=tmp_products)
        db.session.add(order)
        db.session.commit()

        self.create_corresponding_purchases(
            order=order, tmp_products=tmp_products, tmp_quantities=tmp_quantities, tmp_prices=tmp_prices)

        return order
    # @
    #
    def create_products_for_specific_order(self, order, tmp_products):

        for i in range(0, len(tmp_products)):
            product = Product.query.get(tmp_products[i])
            order.selected_products.append(product)
        return order

    #########################################
    #

    def delete_every_order_dependencies(self, order):
        # delete Line relation to recreate
        Line.query.filter(Line.order_id == order.id).delete()

        # TODO : missing delete seller order !!!!

    # @
    #
    def create_order_with_his_products(self, order, tmp_products):

        for i in range(0, len(tmp_products)):
            product = Product.query.get(tmp_products[i])
            order.selected_products.append(product)
        return order

    # @
    #
    def create_corresponding_purchases(self, order, tmp_products, tmp_quantities, tmp_prices):

        for i in range(0, len(tmp_products)):
            bought_item = Line.query.filter(Line.order_id == order.id).filter(
                Line.product_id == tmp_products[i]).first()
            bought_item.quantity = tmp_quantities[i]
            bought_item.price = tmp_prices[i]

    # @
    #
    def get_sellers_from_products(self, order):
        sellerIds = set()
        for product in order.selected_products:
            sellerIds.add(product.seller_id)
        return sellerIds

    # @
    #
    def update_order_status(self, order_id, order_status, payment_status, shipping_status):
        order = Order.query.get_or_404(order_id)

        if order_status != None:
            order.status = order_status

        if(payment_status != None):
            order.payment_status = payment_status

        order.shipping_status = shipping_status

        db.session.commit()

    # @
    #

    def calculate_shipping(self, order):
        base_shipping_price_bases = ''' [{"nb":1, "price":0.6}, {"nb":2, "price":1.16},{"nb":3, "price":1.62}, {"nb":4, "price":2.05}, {"nb":5, "price":2.20}, {"nb":6, "price":2.70}] '''
        prices = json.loads(base_shipping_price_bases)

        customer = Customer.query.get_or_404(order.customer_id)
        nb_products = len(order.lines)
        shipping_price = 0.00
        rules_detail = ''

        if nb_products < 7:
            rules_detail += 'inferieur a 7 articles et '
            for base in prices:
                if base['nb'] == nb_products:
                    shipping_price = float(base['price'])
            if customer.city.lower() != 'langlade':
                rules_detail += 'en dehors de langlade 0,05 par articles en sup'
                shipping_price += 0.05 * nb_products
            else:
                rules_detail += 'commune de langlade pas de supplement '

        else:
            rules_detail += 'superieur a 7 articles et '
            shipping_price = 0, 60 + 0, 40 * (nb_products-1)
            if customer.city.lower() != 'langlade':
                rules_detail += 'en dehors de langlade 0,05 par articles en sup '
                shipping_price += 0.05 * nb_products
            else:
                rules_detail += 'commune de langlade pas de supplement '

        return shipping_price, rules_detail
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

    def get_some(self,  customer_id=0, period=Period_Enum.ALL.value):
        start,end = dates_range(period)
        return OrderDao.read_some(customer_id=customer_id, start=start, end=end)

    def get_one(self,  order_id):
        return OrderDao.read_one(order_id)
