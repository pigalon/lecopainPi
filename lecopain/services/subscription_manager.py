from datetime import datetime

from lecopain.app import app, db
from lecopain.dao.models import Customer, Subscription, Order
from lecopain.dao.shipment_dao import ShipmentDao
from lecopain.dao.subscription_dao import SubscriptionDao
from lecopain.dao.subscription_day_dao import SubscriptionDayDao
from lecopain.helpers.date_utils import dates_range, Period_Enum
from lecopain.services.business_service import BusinessService
from lecopain.services.shipment_manager import ShipmentManager
from datetime import timedelta
from lecopain.dao.models import Category_Enum

class SubscriptionManager():

    businessService = BusinessService()
    shipmentServices = ShipmentManager()

    def duplicate_subscription(self, subscription_id, subscription):
        existing_subscription = SubscriptionDao.get_one(subscription_id)
        created_subscription = SubscriptionDao.add(subscription)
        created_subscription.category = existing_subscription.category
        db.session.flush()
        for subscription_day in existing_subscription.days:
            created_day = SubscriptionDayDao.add(created_subscription.id, subscription_day.day_of_week)
            created_day.nb_products = subscription_day.nb_products
            created_day.price = subscription_day.price
            created_day.shipping_price = subscription_day.shipping_price
            SubscriptionDayDao.add_existing_lines(created_day, subscription_day.lines)


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

    def get_some(self,  customer_id=0, day=datetime.utcnow, period=Period_Enum.ALL.value):
        datetime_day = datetime.strptime(day, '%d%m%Y')
        start, end = dates_range(period, datetime_day)
        return SubscriptionDao.read_some(customer_id=customer_id, start=start, end=end)
    
    def get_some_pagination(self,  customer_id=0, day=datetime.utcnow, period=Period_Enum.ALL.value, page=1, per_page=10):
        datetime_day = datetime.strptime(day, '%d%m%Y')
        start, end = dates_range(period, datetime_day)
        return SubscriptionDao.read_some_pagination(customer_id=customer_id, start=start, end=end, page=page, per_page=per_page)

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
    def create_day_and_parse_line(self, subscription_day, lines, category=Category_Enum.ARTICLE.value):
        parsed_lines = self.parse_lines(lines)
        self.create_day(subscription_day, parsed_lines, category)

    # @
    #
    def create_day(self, subscription_day, lines, category=Category_Enum.ARTICLE.value):
        id = subscription_day.get('id')
        subscription_day_db = SubscriptionDayDao.get_one(id)
        SubscriptionDayDao.add_lines(subscription_day_db, lines)
        
        if subscription_day_db.subscription.category == 'INIT':
            subscription_day_db.subscription.category = category
            db.session.commit()
        
        subscription_day_db.shipping_price, subscription_day_db.shipping_rules = self.businessService.apply_rules_for_subscription_day(
            subscription_day_db)
        
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

        while current_dt <= subscription.end_dt:
            week_day = current_dt.weekday()+1
            subscription_day = self.get_week_day(
                subscription_id=subscription.id, week_day=week_day)

            shipment = {'title': f'abo {subscription.id} - {nb_days}/{delta.days}',
                'customer_id': subscription.customer_id,
                'shipping_dt': current_dt,
                'subscription_id': subscription.id,
                'category' : subscription.category,
            }
            nb_products = subscription_day.get('nb_products')
            lines = []
            if nb_products > 0:
                for line in subscription_day.get('lines') :
                    lines.append({'product_id': line.get('product_id'), 'seller_id': line.get('seller_id'), 'quantity': line.get(
                        'quantity'), 'price': line.get('price')})
                    
                self.shipmentServices.create_shipment(shipment, lines)
            #increment day
            current_dt = current_dt + timedelta(days=1)
            nb_days = nb_days + 1

    def delete_all_shipments(self, subscription):
        for shipment in subscription.shipments:
            ShipmentDao.delete(shipment.id)
        subscription.nb_products = 0
        subscription.nb_orders = 0
        subscription.price = 0.0
        subscription.shipping_price = 0.0
        subscription.nb_shipments = 0
        db.session.commit()








