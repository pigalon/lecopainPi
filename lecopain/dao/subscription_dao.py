from lecopain.app import db
from sqlalchemy import or_, and_
from datetime import datetime

from lecopain.dao.models import (
    Subscription, Customer, SubscriptionSchema, CompleteSubscriptionSchema
)

class SubscriptionDao:

    @staticmethod
    def read_all():

        # Create the list of people from our data

        all_subscriptions = Subscription.query \
            .subscription_by(Subscription.shipping_dt.desc()) \
            .all()

        # Serialize the data for the response
        subscription_schema = SubscriptionSchema(many=True)
        return subscription_schema.dump(all_subscriptions)

    @staticmethod
    def add(subscription):
        customer = Customer.query.get_or_404(int(subscription.get('customer_id')))
        created_subscription = Subscription(customer_id=subscription.get('customer_id'),
                                            seller_id=subscription.get(
                                                'seller_id'),
                            start_dt=subscription.get('start_dt'),
                            end_dt=subscription.get('end_dt'))
        db.session.add(created_subscription)
        return created_subscription

    @staticmethod
    def read_some(customer_id, start, end):
        all_subscriptions = Subscription.query

        if(start !=0):
            startDate = start.date()
            endDate = end.date()

            all_subscriptions = all_subscriptions.filter(
                ((Subscription.start_dt >= startDate) & (Subscription.start_dt <= endDate))
                | ((Subscription.end_dt >= start) & (Subscription.end_dt <= end)))

        if customer_id != 0:
            all_subscriptions = all_subscriptions.filter(
                Subscription.customer_id == customer_id)

        all_subscriptions = all_subscriptions.order_by(Subscription.start_dt.desc()) \
            .all()

        # Serialize the data for the response
        subscription_schema = SubscriptionSchema(many=True)
        return subscription_schema.dump(all_subscriptions)
    
    @staticmethod
    def read_one(id):

        # Create the list of people from our data
        subscription = Subscription.query.get_or_404(id)

        # Serialize the data for the response
        subscription_schema = CompleteSubscriptionSchema(many=False)
        return subscription_schema.dump(subscription)
    
    @staticmethod
    def delete(id):
        subscription = Subscription.query.get_or_404(id)
        db.session.delete(subscription)
        db.session.commit()


