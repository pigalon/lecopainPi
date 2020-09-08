from lecopain.app import db
from sqlalchemy import or_, and_
from datetime import datetime

from lecopain.dao.models import (
    Subscription, Customer, Seller, SubscriptionSchema, CompleteSubscriptionSchema
)

class SubscriptionDao:

    @staticmethod
    def read_all():

        # Create the list of people from our data

        all_subscriptions = Subscription.query \
            .order_by(Subscription.id.desc()) \
            .all()

        # Serialize the data for the response
        subscription_schema = SubscriptionSchema(many=True)
        return subscription_schema.dump(all_subscriptions)

    @staticmethod
    def read_all_by_customer(customer_id):
        all_subscriptions = Subscription.query \
            .filter(Subscription.customer_id == customer_id) \
            .order_by(Subscription.id.desc()) \
            .all()

        # Serialize the data for the response
        subscription_schema = SubscriptionSchema(many=True)
        return subscription_schema.dump(all_subscriptions)

    @staticmethod
    def read_all_by_seller(seller_id):
        all_subscriptions = Subscription.query \
            .filter(Subscription.seller_id == seller_id) \
            .order_by(Subscription.id.desc()) \
            .all()

        # Serialize the data for the response
        subscription_schema = SubscriptionSchema(many=True)
        return subscription_schema.dump(all_subscriptions)

    @staticmethod
    def add(subscription):
        customer = Customer.query.get_or_404(int(subscription.get('customer_id')))
        created_subscription = Subscription(customer_id=subscription.get('customer_id'),
                            start_dt=subscription.get('start_dt'),
                            end_dt=subscription.get('end_dt'),
                            category='INIT')
        db.session.add(created_subscription)
        customer.nb_subscriptions = customer.nb_subscriptions + 1
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

        all_subscriptions = all_subscriptions.order_by(Subscription.id.desc()) \
            .all()

        # Serialize the data for the response
        subscription_schema = SubscriptionSchema(many=True)
        return subscription_schema.dump(all_subscriptions)
    
    @staticmethod
    def read_some_pagination(customer_id, start, end, page, per_page):
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

        all_subscriptions = all_subscriptions.order_by(Subscription.id.desc()) \
            .paginate(page=page, per_page=per_page)

        # Serialize the data for the response
        subscription_schema = SubscriptionSchema(many=True)
        return subscription_schema.dump(all_subscriptions.items), all_subscriptions.prev_num, all_subscriptions.next_num

    @staticmethod
    def read_one(id):
        # Create the list of people from our data
        subscription = Subscription.query.get_or_404(id)
        # Serialize the data for the response
        subscription_schema = CompleteSubscriptionSchema(many=False)
        return subscription_schema.dump(subscription)

    @staticmethod
    def get_one(id):
        return Subscription.query.get_or_404(id)

    @staticmethod
    def delete(id):
        subscription = Subscription.query.get_or_404(id)
        customer = Customer.query.get_or_404(subscription.customer.id)
        db.session.delete(subscription)
        customer.nb_subscriptions = customer.nb_subscriptions - 1
        db.session.commit()

    @staticmethod
    def update_db(subscription, items):
        for item in items:
            setattr(subscription, item['name'], item['value'])
        db.session.commit()
        
    @staticmethod
    def count_by_customer(customer_id):
        return Subscription.query \
            .filter(Subscription.customer_id == customer_id) \
            .order_by(Subscription.start_dt.desc()) \
            .count()


