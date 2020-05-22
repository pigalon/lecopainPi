from lecopain.app import db
from sqlalchemy import or_, and_
from datetime import datetime

from lecopain.dao.models import (
    SubscriptionDay, Customer, SubscriptionDaySchema, CompleteSubscriptionDaySchema
)


class SubscriptionDayDao:


    @staticmethod
    def add(subscription_id, number):
        created_subscription_day = SubscriptionDay(subscription_id=subscription_id,
                                            day_of_week =number)
        db.session.add(created_subscription_day)
        return created_subscription_day

    @staticmethod
    def read_one(id):
        subscription_day = SubscriptionDay.query.get_or_404(id)
        subscription_schema = CompleteSubscriptionDaySchema(many=False)
        return subscription_schema.dump(subscription_day)

    @staticmethod
    def delete(id):
        subscription_day = SubscriptionDay.query.get_or_404(id)
        db.session.delete(subscription_day)
        db.session.commit()


