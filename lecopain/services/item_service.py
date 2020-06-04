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

    def add_order_subscription_nb_orders(self, subscription, nb_orders):
        self.items.append(
            {'name': 'nb_orders', 'value': (subscription.nb_orders + nb_orders)})
        return self

    def add_order_subscription_nb_products(self, subscription, nb_products):
        self.items.append(
            {'name': 'nb_products', 'value': (subscription.nb_products + nb_products)})
        return self

    def add_order_subscription_shipping_price(self, subscription, shipping_price):
        self.items.append({'name': 'shipping_price',
                      'value': (subscription.shipping_price + shipping_price)})
        return self

    def add_order_subscription_price(self, subscription, price):
        self.items.append({'name': 'price', 'value': (
            subscription.price + price)})
        return self

    def remove_order_subscription_nb_orders(self, subscription, nb_orders):
        self.items.append(
            {'name': 'nb_orders', 'value': (subscription.nb_orders - nb_orders)})
        return self

    def remove_order_subscription_nb_products(self, subscription, nb_products):
        self.items.append(
            {'name': 'nb_products', 'value': (subscription.nb_products - nb_products)})
        return self

    def remove_order_subscription_shipping_price(self, subscription, shipping_price):
        self.items.append({'name': 'shipping_price',
                           'value': (subscription.shipping_price - shipping_price)})
        return self

    def remove_order_subscription_price(self, subscription, price):
        self.items.append({'name': 'price', 'value': (
            subscription.price - price)})
        return self






