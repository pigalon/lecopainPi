from lecopain.app import db

from lecopain.dao.models import (
    Subscription, Customer, SubscriptionSchema
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
                            start_dt=subscription.get('start_dt'),
                            end_dt=subscription.get('end_dt'))
        db.session.add(created_subscription)
        return created_subscription

