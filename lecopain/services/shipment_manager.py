from datetime import datetime, date, timedelta

from lecopain.app import app, db
from lecopain.services.business_service import BusinessService
from lecopain.services.item_service import ItemService
from lecopain.services.order_manager import OrderManager
from lecopain.dao.models import Line, Product, Seller, Customer, Shipment, ShipmentStatus_Enum, Category_Enum
from lecopain.helpers.date_utils import dates_range, Period_Enum
from lecopain.dao.shipment_dao import ShipmentDao
from lecopain.dao.subscription_dao import SubscriptionDao
from lecopain.dao.product_dao import ProductDao
import json
from sqlalchemy import extract, Date, cast

class ShipmentManager():

    businessService = BusinessService()
    itemService = ItemService()
    orderService = OrderManager()

    def parse_lines(self, lines):
        headers = ('product_id', 'seller_id', 'quantity', 'price' )
        items = [{} for i in range(len(lines[0]))]
        for x, i in enumerate(lines):
            for _x, _i in enumerate(i):
                items[_x][headers[x]] = _i
        return items

    def sort_lines_by_seller(self, lines):
        sorted_lines = []
        for line in lines:
            res_line = [sorted_line for sorted_line in sorted_lines if sorted_line["seller_id"] == line['seller_id']]
            new_line = {'product_id':line['product_id'],'quantity':line['quantity'],'price':line['price'] }

            if len(res_line)>0 :
                res_line[0]['lines'].append(new_line)
            else:
                sorted_lines.append({'seller_id' : line['seller_id'], 'lines' : [new_line]})

        return sorted_lines
    
    def create_shipment_and_parse_line(self, shipment, lines):
        parsed_lines = self.parse_lines(lines)
        self.create_shipment(shipment, parsed_lines)

    def create_shipment(self, shipment, lines):
        created_shipment = ShipmentDao.create_shipment(shipment)
        sorted_lines = self.sort_lines_by_seller(lines)
        for grouped_lines in sorted_lines:
            self.orderService.create_by_shipment(created_shipment, grouped_lines['lines'], grouped_lines['seller_id'])
            db.session.commit()
            if created_shipment.category != Category_Enum.PRESTATION.value:
                created_shipment.shipping_price, created_shipment.shipping_rules = self.businessService.apply_rules_for_shipment(
            created_shipment)
            else :
                created_shipment.shipping_price, created_shipment.shipping_rules = self.businessService.prestation_rules_for_shipment(
            created_shipment)
            db.session.commit()
        if created_shipment.subscription_id is not None :
            self.items_add_subscription(created_shipment)

    def delete_shipment(self, shipment_id):
        shipment = ShipmentDao.get_one(shipment_id)
        if shipment.subscription_id is not None:
            self.remove_shipment_subscriptions(shipment)
        ShipmentDao.delete(shipment_id)
        ShipmentDao.update_db(shipment)

    def update_shipment_and_parse_line(self, shipment_id, lines):
        shipment = ShipmentDao.get_one(shipment_id)
        
        #remove shipment from subscription
        if shipment.subscription != None:
            self.remove_shipment_subscriptions(shipment)
        
        # init to 0 shipment
        shipment.init_stats()  

        parsed_lines = self.parse_lines(lines)
        sorted_lines = self.sort_lines_by_seller(parsed_lines)

        for order in shipment.orders:
            b_delete = True
            for grouped_lines in sorted_lines:
                if str(order.seller_id) == grouped_lines['seller_id']:
                    b_delete = False
            if(b_delete):
                shipment.remove_order(order)

        for grouped_lines in sorted_lines:
            self.orderService.update_by_shipment(shipment, grouped_lines['lines'], grouped_lines['seller_id'])

        shipment.shipping_price, shipment.shipping_rules = self.businessService.apply_rules_for_shipment(
            shipment)
        
        shipment.updated_at = datetime.now()
        
        if shipment.subscription != None:
            self.add_shipment_subscriptions(shipment)

        db.session.commit()

    def remove_shipment_subscriptions(self, shipment):
        subscription = SubscriptionDao.get_one(shipment.subscription_id)
        itemService = ItemService()
        itemService.decrement_subscription_nb_shipments(subscription) \
            .remove_shipment_subscription_nb_products(subscription, shipment.nb_products) \
            .remove_shipment_subscription_shipping_price(subscription, shipment.shipping_price) \
            .remove_shipment_subscription_nb_orders(subscription, shipment.nb_orders)
        SubscriptionDao.update_db(subscription, itemService.items)
    
    def add_shipment_subscriptions(self, shipment):
        subscription = SubscriptionDao.get_one(shipment.subscription_id)
        itemService = ItemService()
        itemService.increment_subscription_nb_shipments(subscription) \
            .add_shipment_subscription_nb_products(subscription, shipment.nb_products) \
            .add_shipment_subscription_shipping_price(subscription, shipment.shipping_price) \
            .add_shipment_subscription_nb_orders(subscription, shipment.nb_orders)
        SubscriptionDao.update_db(subscription, itemService.items)


    def items_remove_subscription(self, shipment):
        subscription = SubscriptionDao.get_one(shipment.subscription_id)
        itemService = ItemService()
        itemService.remove_shipment_subscription_nb_products(subscription, shipment.nb_products) \
            .remove_shipment_subscription_shipping_price(subscription, shipment.shipping_price) \
            .decrement_subscription_nb_shipments(subscription) \
            .remove_shipment_subscription_nb_orders(subscription, shipment.nb_orders)
        SubscriptionDao.update_db(subscription, itemService.items)

    def items_add_subscription(self, shipment):
        subscription = SubscriptionDao.get_one(shipment.subscription_id)
        itemService = ItemService()
        itemService.add_shipment_subscription_nb_products(subscription, shipment.nb_products) \
            .add_shipment_subscription_shipping_price(subscription, shipment.shipping_price) \
            .increment_subscription_nb_shipments(subscription) \
            .add_shipment_subscription_nb_orders(subscription, shipment.nb_orders)
        SubscriptionDao.update_db(subscription, itemService.items)

    # @
    #
    def update_shipment_status(self, shipment_id, shipment_status):
        shipment = ShipmentDao.get_one(shipment_id)
        if shipment.status != shipment_status:
            if shipment_status == ShipmentStatus_Enum.ANNULEE.value and shipment.subscription_id is not None:
                self.items_remove_subscription(shipment)

            if shipment_status == ShipmentStatus_Enum.CREE.value and shipment.subscription_id is not None:
                self.items_add_subscription(shipment)

            ShipmentDao.update_status(shipment_id, shipment_status)

    # @
    #
    def update_shipment_shipping_status(self, shipment_id, shipping_status):
        ShipmentDao.update_shipping_status(shipment_id, shipping_status)

    # @
    #
    def update_shipment_payment_status(self, shipment_id, payment_status):
        ShipmentDao.update_payment_status(shipment_id, payment_status)

    # @
    #
    def get_in_progess_shipments_counter(self):
        return Shipment.query.filter(Shipment.status == ShipmentStatus_Enum.CREE.value).count()

    # @
    #
    def get_latest_shipments_counter(self):
        date_since_2_days = date.today() - timedelta(days=2)
        return Shipment.query.filter(Shipment.created_at > date_since_2_days).count()

    def get_all(self):
        return ShipmentDao.read_all()

    def get_all_by_subscription(self, subscription_id):
        return ShipmentDao.read_by_subscription(subscription_id)

    def get_all_by_customer(self, customer_id):
        return ShipmentDao.read_by_customer(customer_id)

    def get_some(self,  customer_id=0, day=datetime.utcnow, period=Period_Enum.ALL.value):
        datetime_day = datetime.strptime(day, '%d%m%Y')
        start, end = dates_range(period, datetime_day)
        return ShipmentDao.read_some(customer_id=customer_id, start=start, end=end)

    def get_one(self,  shipment_id):
        return ShipmentDao.read_one(shipment_id)

    def get_shipment_status(self):
        return list(map(lambda c: c.value, ShipmentStatus_Enum))

    def update_shipping_dt(self, shipment, shipping_dt):
        ShipmentDao.update_shipping_dt(shipment['id'], shipping_dt)

    def find(self, products, short_name):
        for product in products: 
            if product['short_name'] == short_name: 
                return product
        return None

    def extract_products_from_shipments(self, shipments):
        products = []
        product = None
        for shipment in shipments:
            for line in shipment['lines']:
                short_name = line['product_short_name']
                quantity  = line['quantity']
                product = self.find(products, short_name) 
                if product != None:
                    #line_tmp = [d for d in shipment['lines'] if d['line']['product_short_name'] == short_name]
                    product['quantity'] = product['quantity'] + int(line['quantity'])
                else :
                    products.append({'short_name':line['product_short_name'], 'quantity':int(line['quantity'])})
        return products




