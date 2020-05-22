from datetime import datetime

from lecopain.app import app, db
from lecopain.dao.models import Customer, Subscription
from lecopain.dao.subscription_dao import SubscriptionDao
from lecopain.dao.subscription_day_dao import SubscriptionDayDao
from lecopain.helpers.date_utils import dates_range, Period_Enum


class SubscriptionManager():

    def create_subscription(self, subscription):
        created_subscription = SubscriptionDao.add(subscription)
        db.session.flush()
        self.create_subscription_days(created_subscription.id)
        db.session.commit()

    def create_subscription_days(self, subscription_id):
        nb_days = 7
        for number in range(1,nb_days):
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


    def delete_subscription(self, subscription_id):
        SubscriptionDao.delete(subscription_id)


