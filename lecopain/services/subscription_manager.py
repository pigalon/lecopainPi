from datetime import datetime

from lecopain.app import app, db
from lecopain.dao.models import Customer, Subscription
from lecopain.dao.subscription_dao import SubscriptionDao
from lecopain.helpers.date_utils import dates_range, Period_Enum


class SubscriptionManager():

    def create_subscription(self, subscription):
        created_subscription = SubscriptionDao.add(subscription)
        db.session.commit()

    def get_all(self):
        return SubscriptionDao.read_all()

    def get_some(self,  customer_id=0, period=Period_Enum.ALL.value):
        start, end = dates_range(period)
        return SubscriptionDao.read_some(customer_id=customer_id, start=start, end=end)

    def get_one(self,  subscription_id):
        return SubscriptionDao.read_one(subscription_id)
