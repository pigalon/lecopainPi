class ItemService:

    items = []
    def increment_subscription_nb_order(self, subscription):
        self.items.append(
            {'name': 'nb_orders', 'value': (subscription.nb_orders + 1)})
        return self

    def decrement_subscription_nb_order(self, subscription):
        self.items.append(
            {'name': 'nb_orders', 'value': (subscription.nb_orders - 1)})
        return self

    def add_order_subscription_nb_products(self, subscription, order):
        self.items.append(
            {'name': 'nb_products', 'value': (subscription.nb_products + order.nb_products)})
        return self

    def add_order_subscription_shipping_price_products(self, subscription, order):
        self.items.append({'name': 'shipping_price',
                      'value': (subscription.shipping_price + order.shipping_price)})
        return self

    def add_order_subscription_price_products(self, subscription, order):
        self.items.append({'name': 'price', 'value': (
            subscription.price + order.price)})
        return self







