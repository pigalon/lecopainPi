from datetime import datetime

from lecopain.app import app, db
from lecopain.dao.models import Customer, Subscription, Order
from lecopain.dao.order_dao import OrderDao
from lecopain.dao.subscription_dao import SubscriptionDao
from lecopain.dao.subscription_day_dao import SubscriptionDayDao
from lecopain.helpers.date_utils import dates_range, Period_Enum
from lecopain.services.business_service import BusinessService
from lecopain.services.shipment_manager import ShipmentManager
from datetime import timedelta


class SubscriptionManager():

    businessService = BusinessService()
    shipmentServices = ShipmentManager()

    def create_subscription(self, subscription):
        created_subscription = SubscriptionDao.add(subscription)
        db.session.flush()
        self.create_subscription_days(created_subscription.id)
        db.session.commit()

    def create_subscription_days(self, subscription_id):
        nb_days = 7
        for number in range(1, nb_days+1):
            SubscriptionDayDao.add(subscription_id, number)


    def get_all(self):
        return SubscriptionDao.read_all()

    def get_all_by_customer(self, customer_id):
        return SubscriptionDao.read_all_by_customer(customer_id)

    def get_all_by_seller(self, seller_id):
        return SubscriptionDao.read_all_by_seller(seller_id)


    def get_some(self,  customer_id=0, period=Period_Enum.ALL.value):
        start, end = dates_range(period)
        return SubscriptionDao.read_some(customer_id=customer_id, start=start, end=end)

    def get_one(self,  subscription_id):
        return SubscriptionDao.read_one(subscription_id)

    def get_one_db(self,  subscription_id):
        return SubscriptionDao.get_one(subscription_id)

    def get_one_day(self,  subscription_day_id):
        return SubscriptionDayDao.read_one(subscription_day_id)

    def get_week_day(self, subscription_id, week_day):
        return SubscriptionDayDao.get_one_by_week_day(subscription_id, week_day)


    def delete_subscription(self, subscription_id):
        SubscriptionDao.delete(subscription_id)

    def parse_lines(self, lines):
        headers = ('product_id', 'seller_id', 'quantity', 'price' )
        items = [{} for i in range(len(lines[0]))]
        for x, i in enumerate(lines):
            for _x, _i in enumerate(i):
                items[_x][headers[x]] = _i
        return items

    # @
    #
    def create_day_and_parse_line(self, subscription_day, lines):
        parsed_lines = self.parse_lines(lines)
        self.create_day(subscription_day, parsed_lines)

    # @
    #
    def create_day(self, subscription_day, lines):
        id = subscription_day.get('id')
        subscription_day_db = SubscriptionDayDao.get_one(id)
        SubscriptionDayDao.add_lines(subscription_day_db, lines)

        subscription_day_complete = SubscriptionDayDao.read_one(id)
        category = SubscriptionDayDao.get_category(subscription_day_complete)
        city = subscription_day_complete.get('customer_city')
        nb_products = subscription_day_complete.get('nb_products')
        subscription_day_db.shipping_price, subscription_day_db.shipping_rules = self.businessService.get_price_and_associated_rules(
            category=category, city=city, nb_products=nb_products)
        subscription_day_db.subscription.category = category
        db.session.commit()

        # @
    #
    def cancel_day(self, subscription_day_id):
        subscription_day_tmp = SubscriptionDayDao.get_one(subscription_day_id)
        subscription_id = subscription_day_tmp.subscription_id
        number = subscription_day_tmp.day_of_week
        SubscriptionDayDao.delete(subscription_day_id)
        subscription_day = SubscriptionDayDao.add(subscription_id, number)
        db.session.commit()
        return subscription_day

    def generate_shipments(self, subscription):
        # get a list from all days fo the periode : dict
        # date_of_day : datetime 8:00
        # get the id of the subscription_day
        # for all days from the list :
        # get the subscription_day
        # create the order (convertion from subscription_day) for the day and for the customer / seller / nb_pducts / prices etc...
        # get all the subscription_lines and (convertion to line)
        week_day  = 0
        current_dt = subscription.start_dt
        delta = subscription.end_dt - subscription.start_dt
        nb_days = 1
        shipment = {}
        total_nb_products = 0
        nb_products = 0
        nb_shipments = 0
        nb_orders = 0
        total_shipping_price = 0.0
        total_price = 0.0


        while current_dt <= subscription.end_dt:
            

            week_day = current_dt.weekday()+1
            subscription_day = self.get_week_day(
                subscription_id=subscription.id, week_day=week_day)

            shipment = {'title': f'abo {subscription.id} - {nb_days}/{delta.days}',
                'customer_id': subscription.customer_id,
                'shipping_dt': current_dt,
                'subscription_id': subscription.id,
                
            }
            nb_products = subscription_day.get('nb_products')
            total_nb_products = total_nb_products + nb_products
            lines = []
            if nb_products > 0:
                for line in subscription_day.get('lines') :
                    lines.append({'product_id': line.get('product_id'), 'seller_id': line.get('seller_id'), 'quantity': line.get(
                        'quantity'), 'price': line.get('price')})
                    
                self.shipmentServices.create_shipment(shipment, lines)
            #increment day
            current_dt = current_dt + timedelta(days=1)
            nb_days = nb_days + 1

        #         created_order = ShipmentDao.create_order(order, lines)
        #         created_order.shipping_price, created_order.shipping_rules = self.businessService.apply_rules(
        #         created_order)
        #         created_order.category = created_order.products[0].category
        #         created_order.subscription_id = subscription.id
        #         OrderDao.update_db(order)
        #         nb_orders = nb_orders + 1
        #         total_shipping_price = total_shipping_price + float(created_order.shipping_price)
        #         total_price = total_price + float(created_order.price)
        #     # increment day
        #     current_dt = current_dt + timedelta(days=1)
        #     nb_days = nb_days + 1
        
        # itemService = ItemService()
        # itemService.add_order_subscription_nb_products(subscription, total_nb_products). \
        # add_order_subscription_nb_orders(subscription, nb_orders). \
        # add_order_subscription_shipping_price(subscription, total_shipping_price). \
        # add_order_subscription_price(subscription, total_price)
        
        # SubscriptionDao.update_db(subscription, itemService.items)






