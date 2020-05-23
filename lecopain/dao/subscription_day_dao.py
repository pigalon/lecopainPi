from lecopain.app import db
from sqlalchemy import or_, and_
from datetime import datetime

from lecopain.dao.models import (
    SubscriptionDay, SubscriptionLine, Customer, SubscriptionDaySchema, CompleteSubscriptionDaySchema
)


class SubscriptionDayDao:

    @staticmethod
    def add(subscription_id, number):
        created_subscription_day = SubscriptionDay(subscription_id=subscription_id,
                                            day_of_week =number)
        db.session.add(created_subscription_day)
        return created_subscription_day

    @staticmethod
    def get_one(id):
        return SubscriptionDay.query.get_or_404(id)

    @staticmethod
    def get_one_by_week_day(subscription_id, week_day):
        subscription_day =  SubscriptionDay.query.filter(
            SubscriptionDay.subscription_id == subscription_id).filter(
              SubscriptionDay.day_of_week == int(week_day)).first()
        subscription_schema = CompleteSubscriptionDaySchema(many=False)
        return subscription_schema.dump(subscription_day)



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

    @staticmethod
    def add_lines(subscription_day, lines):
        nb_products = 0
        total_price = 0.0
        for line in lines:
            product_id, qty, price = list(line.values())
            nb_products = nb_products + int(qty)
            total_price = total_price + int(qty) * float(price)
            subscription_day.lines.append(SubscriptionLine(
                subscription_day=subscription_day, product_id=product_id, quantity=qty, price=float(price)))
        subscription_day.price = format(total_price, '.2f')
        subscription_day.nb_products = nb_products


