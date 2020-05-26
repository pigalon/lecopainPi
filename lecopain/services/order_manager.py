from datetime import datetime, date, timedelta

from lecopain.app import app, db
from lecopain.services.business_service import BusinessService
from lecopain.dao.models import Line, Product, Seller, Customer, Order, OrderStatus_Enum
from lecopain.helpers.date_utils import dates_range, Period_Enum
from lecopain.dao.order_dao import OrderDao
from lecopain.dao.product_dao import ProductDao
import json
from sqlalchemy import extract, Date, cast

class OrderManager():

    businessService = BusinessService()

    def parse_lines(self, lines):
        headers = ('product_id', 'quantity', 'price' )
        items = [{} for i in range(len(lines[0]))]
        for x, i in enumerate(lines):
            for _x, _i in enumerate(i):
                items[_x][headers[x]] = _i
        return items

    def create_order_and_parse_line(self, order, lines):
        parsed_lines = self.parse_lines(lines)
        created_order = OrderDao.create_order(order, parsed_lines)
        created_order.shipping_price, created_order.shipping_rules = self.businessService.apply_rules(
            created_order)
        created_order.category = created_order.products[0].category
        OrderDao.update_db(created_order)

    def delete_order(self, order_id):
        OrderDao.delete(order_id)

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
    def update_order_status(self, order_id, order_status):
        OrderDao.update_status(order_id, order_status)

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

    def get_some(self,  customer_id=0, period=Period_Enum.ALL.value):
        start,end = dates_range(period)
        return OrderDao.read_some(customer_id=customer_id, start=start, end=end)

    def get_one(self,  order_id):
        return OrderDao.read_one(order_id)

    def get_order_status(self):
        return list(map(lambda c: c.value, OrderStatus_Enum))

    def update_shipping_dt(self, order, shipping_dt):
        OrderDao.update_shipping_dt(order['id'], shipping_dt)


