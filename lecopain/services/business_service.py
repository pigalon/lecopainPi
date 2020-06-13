from lecopain.dao.models import Category_Enum
class BusinessService:
    local_shipping_price = {1:0.6, 2:1.16, 3:1.62, 4:2.05, 5:2.20, 6:2.70, 'n':0.40, 'c':5, 'd':8}
    far_shipping_price = {1: 0.65, 2: 1.25,
                          3: 1.75, 4: 2.20, 5: 2.50, 'n': 0.45, 'c': 6, 'd': 8}

    def is_from_local_area(self, city):
        return city.lower() == 'langlade'

    def is_article(self, category):
        return category == Category_Enum.ARTICLE.value

    def is_coursette(self, category):
        return category == Category_Enum.COURSETTE.value

    def is_drive(self, category):
        return category == Category_Enum.DRIVE.value

    def apply_rules_just_order(self, order):
        return self.get_price_and_associated_rules(order.shipment.category, order.shipment.shipping_city, order.nb_products)


    def apply_rules(self, shipment):
        return self.get_price_and_associated_rules(shipment.category, shipment.shipping_city, shipment.nb_products)

    def get_price_and_associated_rules(self, category, city, nb_products=0):
        if self.is_article(category) and self.is_from_local_area(city) and nb_products < 7:
            ret, rules = self.local_shipping_price.get(int(nb_products)), "article_local_"+str(nb_products)

        elif self.is_article(category) and self.is_from_local_area(city) and nb_products >= 7:
            ret, rules = self.local_shipping_price.get(
                1) + (self.local_shipping_price.get('n') * int(nb_products-1)), "article_local_"+str(nb_products)

        elif self.is_article(category) and not self.is_from_local_area(city) and nb_products < 6:
            ret, rules = self.far_shipping_price.get(
                int(nb_products)), "article_non-local_"+str(nb_products)

        elif self.is_article(category) and not self.is_from_local_area(city) and nb_products >= 6:
            ret, rules = self.far_shipping_price.get(1) + (self.far_shipping_price.get(
                'n') * int(nb_products-1)), "article_non-local_"+str(nb_products)

        elif self.is_coursette(category) and self.is_from_local_area(city):
            ret, rules = self.local_shipping_price.get('c'), "coursette_local"

        elif self.is_coursette(category) and not self.is_from_local_area(city):
            ret, rules = self.far_shipping_price.get(
                'c'), "coursette_non-local"

        elif self.is_drive(category) and self.is_from_local_area(city):
            ret, rules = self.local_shipping_price.get('d'), "drive_local"

        elif self.is_drive(category) and not self.is_from_local_area(city):
            ret, rules = self.far_shipping_price.get('d'), "drive_non-local"
        if ret == None:
            ret = 0.0
        return format(ret, '.2f'), rules

