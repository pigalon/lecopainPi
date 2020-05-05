from datetime import datetime

from lecopain.app import app, db
from lecopain.dao.models import Customer, Subscription_product


class SubscriptionManager():

    def first(self):

        print(" shippings 3-pret")

    # @
    #
    def create_subscription(self, subscription, tmp_products, tmp_quantities, tmp_prices):
        products = {}

        subscription = self.create_product_purchases(
            subscription, tmp_products, tmp_quantities, tmp_prices)
        # TODO
        # self.generate_orders(subscription)

    ##############################################
    # MAPS from subscriptions => total and quantity and customer
    ###############################################
    def get_maps_from_subscriptions(self, subscriptions):

        customerMap = {}
        totalMap = {}
        nb_productsMap = {}

        map = {}

        for subscription in subscriptions:
            customer = Customer.query.get_or_404(subscription.customer_id)
            customerMap[subscription.id] = str(
                customer.firstname + " " + customer.lastname)

            bought_items = Subscription_product.query.filter(
                Subscription_product.order_id == subscription.id).all()
            total = 0
            quantity = 0
            for bought_item in bought_items:
                total += bought_item.price * bought_item.quantity
                quantity += bought_item.quantity
            totalMap[subscription.id] = total
            nb_productsMap[subscription.id] = quantity
        map['CUSTOMER'] = customerMap
        map['NB_PRODUCTS'] = nb_productsMap
        map['TOTAL'] = totalMap
        return map
