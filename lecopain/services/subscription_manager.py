from datetime import datetime

from lecopain.app import app, db
from lecopain.dao.models import Customer, Subscription
from lecopain.dao.subscription_dao import SubscriptionDao
from lecopain.dao.subscription_day_dao import SubscriptionDayDao
from lecopain.helpers.date_utils import dates_range, Period_Enum
from lecopain.services.business_service import BusinessService


class SubscriptionManager():
    
    businessService = BusinessService()

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

    def get_some(self,  customer_id=0, period=Period_Enum.ALL.value):
        start, end = dates_range(period)
        return SubscriptionDao.read_some(customer_id=customer_id, start=start, end=end)

    def get_one(self,  subscription_id):
        return SubscriptionDao.read_one(subscription_id)
    
    def get_one_day(self,  subscription_day_id):
        return SubscriptionDayDao.read_one(subscription_day_id)

    def get_week_day(self, subscription_id, week_day):
        return SubscriptionDayDao.get_one_by_week_day(subscription_id, week_day)


    def delete_subscription(self, subscription_id):
        SubscriptionDao.delete(subscription_id)
        
    def parse_lines(self, lines):
        headers = ('product_id', 'quantity', 'price' )
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



