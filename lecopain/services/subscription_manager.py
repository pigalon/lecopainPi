from datetime import datetime

from lecopain.app import app, db
from lecopain.dao.models import Customer, Subscription
from lecopain.dao.subscription_dao import SubscriptionDao


class SubscriptionManager():

    def create_subscription(self, subscription):
        created_subscription = SubscriptionDao.add(subscription)
        db.session.commit()

    def get_all(self):
        return SubscriptionDao.read_all()
