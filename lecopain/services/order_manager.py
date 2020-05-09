from datetime import datetime, date, timedelta

from lecopain.app import app, db
from lecopain.dto.BoughtProduct import BoughtProduct
from lecopain.dao.models import Shipping, Line, Product, Seller, SellerOrder, Customer, Order, OrderStatus_Enum
from lecopain.helpers.date_utils import get_start_and_end_date_from_calendar_week, get_start_and_end_date_from_calendar_month
import json
from sqlalchemy import extract


class OrderManager():

    ##############################################
    # Orders list ordered by date
    ###############################################
    def build_orders_list(self, customer_id, date_tab):
        year, month, day = date_tab

        if(year == 0):
            year = datetime.now().year

        if(month == 0):
            month = datetime.now().month

        if(day == 0):
            day = datetime.now().day

        orders = None

        if customer_id != 0 and customer_id is not None:
            orders = Order.query.filter(
                Order.customer_id == customer_id)

        orders = Order.query.filter(
            extract('year', Order.shipping_dt) == year).filter(
                extract('month', Order.shipping_dt) == month)

        if day is not None:
            orders = orders.filter(
                extract('day', Order.shipping_dt) == day)

        return orders.all()

    ##############################################
    # Orders by customer
    ###############################################
    def orders_by_customer(self, orders, customer_id):
        orders.filter(
            Order.customer_id == customer_id)

    ##############################################
    # Orders by desc date
    ###############################################
    def orders_by_date_desc(self, orders):
        orders.order_by(
            Order.shipping_dt.desc()).all()

    ##############################################
    # Orders list ordered by date for the current month
    ###############################################
    def orders_of_the_month(self, customer_id=0):

        today = datetime.today()

        start_date, end_date = get_start_and_end_date_from_calendar_month(
            today.year, today.month)

        orders = Order.query.filter(
            Order.shipping_dt >= start_date).filter(
            Order.shipping_dt <= end_date)

        if customer_id != 0:
            orders_by_customer(orders, customer_id)

        self.orders_by_date_desc(orders)

        return orders.all()

    ##############################################
    # Orders list ordered by date for the current week
    ###############################################
    def orders_of_the_week(self, customer_id=0):

        today = datetime.today()

        start_date, end_date = get_start_and_end_date_from_calendar_week(
            today.year, today.weekday())

        orders = Order.query.filter(
            Order.shipping_dt >= start_date).filter(
            Order.shipping_dt <= end_date)

        if customer_id != 0:
            orders_by_customer(orders, customer_id)

        self.orders_by_date_desc(orders)

        return orders.all()

    ##############################################
    # Orders list ordered by date for the current day
    ###############################################
    def orders_of_the_day(self, customer_id=0):

        today = datetime.today()

        orders = Order.query.filter(
            Order.shipping_dt == today)

        if customer_id != 0:
            orders_by_customer(orders, customer_id)

        self.orders_by_date_desc(orders)

        return orders.all()

    ##############################################
    # All orders
    ###############################################
    def all_orders(self, customer_id=0):
        orders = Order.query

        if customer_id != 0:
            orders_by_customer(orders, customer_id)

        self.orders_by_date_desc(orders)

        return orders.all()

    ##############################################
    # products list from order
    ###############################################

    def get_resume_products_list_from_orders(self, orders):
        products = []
        for order in orders:
            for product in order.selected_products:

                line = Line.query.filter(Line.order_id == order.id).filter(
                    Line.product_id == product.id).first()

                bAdded = False

                if product in products:
                    products[products.index(product)].quantity += line.quantity
                    bAdded = True

                if(len(products) < 1 or bAdded == False):
                    products.append(BoughtProduct(
                                    product=product, quantity=line.quantity))
        return products

    ##############################################
    # MAPS from ORDERS => total and quantity and customer
    ###############################################
    def get_maps_from_orders(self, orders):

        customerMap = {}
        totalMap = {}
        nb_productsMap = {}

        map = {}

        for order in orders:
            customer = Customer.query.get_or_404(order.customer_id)
            customerMap[order.id] = str(
                customer.firstname + " " + customer.lastname)

            bought_items = Line.query.filter(Line.order_id == order.id).all()
            total = 0
            quantity = 0
            for bought_item in bought_items:
                total += bought_item.price * bought_item.quantity
                quantity += bought_item.quantity

            totalMap[order.id] = total
            nb_productsMap[order.id] = quantity

        map['CUSTOMER'] = customerMap
        map['NB_PRODUCTS'] = nb_productsMap
        map['TOTAL'] = totalMap

        return map

    # @
    #
    def create_order(self, order, tmp_products, tmp_quantities, tmp_prices):
        order.created_at = datetime.now()
        order = self.create_product_purchases(
            order, tmp_products, tmp_quantities, tmp_prices)
        self.create_default_shipping(order)

    # @
    #
    def update_order(self, order, products, quantities, prices):

        order.created_at = datetime.now()
        self.delete_every_order_dependencies(order)
        order = self.create_product_purchases(
            order, products, quantities, prices)
        db.session.commit()

    # @
    #

    def create_product_purchases(self, order, tmp_products, tmp_quantities, tmp_prices):
        order = self.create_products_for_specific_order(
            order=order, tmp_products=tmp_products)
        db.session.add(order)
        db.session.commit()

        self.create_corresponding_purchases(
            order=order, tmp_products=tmp_products, tmp_quantities=tmp_quantities, tmp_prices=tmp_prices)

        sellerOrders = self.generate_seller_orders(order=order)
        for sellerOrder in sellerOrders:
            db.session.add(sellerOrder)
        return order
    # @
    #
    def create_products_for_specific_order(self, order, tmp_products):

        for i in range(0, len(tmp_products)):
            product = Product.query.get(tmp_products[i])
            order.selected_products.append(product)
        return order

    ##########################################
    #
    def create_default_shipping(self, order):
        shipping = Shipping(reference=order.title, shipping_dt=order.shipping_dt,
                            status='NON_LIVREE', order_id=order.id, customer_id=order.customer_id)
        db.session.add(shipping)
        db.session.commit()

    #########################################
    #

    def delete_every_order_dependencies(self, order):
        # delete Line relation to recreate
        Line.query.filter(Line.order_id == order.id).delete()

        # TODO : missing delete seller order !!!!
        SellerOrder.query.filter(
            SellerOrder.order_id == order.id).delete()

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
    def generate_seller_orders(self, order):
        sellerOrders = []
        sellerIds = self.get_sellers_from_products(order)
        for sellerId in sellerIds:
            sellerOrders.append(SellerOrder(
                title=order.title, status='CREE', order_id=order.id, seller_id=sellerId))

        return sellerOrders

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

        shipping = Shipping.query.filter(
            Shipping.order_id == order_id).first()
        if shipping != None and shipping_status != None:
            shipping.status = shipping_status

        sellerOrders = SellerOrder.query.filter(
            SellerOrder.order_id == order_id).all()
        for sellerOrder in sellerOrders:
            if order_status != None:
                sellerOrder.status = order_status

        db.session.commit()

    # @
    #

    def calculate_shipping(self, order):
        base_shipping_price_bases = ''' [{"nb":1, "price":0.6}, {"nb":2, "price":1.16},{"nb":3, "price":1.62}, {"nb":4, "price":2.05}, {"nb":5, "price":2.20}, {"nb":6, "price":2.70}] '''
        prices = json.loads(base_shipping_price_bases)

        customer = Customer.query.get_or_404(order.customer_id)
        nb_products = len(order.selected_products)
        shipping_price = 0.00
        rules_detail = ''

        if nb_products < 7:
            rules_detail += 'inferieur a 7 articles et '
            for base in prices:
                print('base : ' + str(base['nb']))
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
