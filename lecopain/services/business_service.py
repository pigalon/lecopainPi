from lecopain.dao.models import Category_Enum
from lecopain.dao.models import OrderStatus_Enum
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

    # def apply_rules_just_order(self, order):
    #     return self.get_price_and_associated_rules(order.shipment.category, order.shipment.shipping_city, order.seller.city, order.nb_products)


    def apply_rules_for_subscription_day(self, subscription_day):
        amount = 0.0
        nb_local_products = 0
        nb_far_products = 0
                
        # for order in subscription_day:
        #     if(self.is_from_local_area(order.seller_city) and self.is_from_local_area(shipment.shipping_city)):
        #         nb_local_products = nb_local_products + order.nb_products
        #     else:
        #         nb_far_products = nb_far_products + order.nb_products
                
        # return self.get_price_and_associated_rules(shipment.category, nb_local_products, nb_far_products)

    def apply_rules_for_shipment(self, shipment):
        amount = 0.0
        nb_local_products = 0
        nb_far_products = 0
                
        for order in shipment.orders:
            if order.status != OrderStatus_Enum.ANNULEE.value:
                if(self.is_from_local_area(order.seller.city) and self.is_from_local_area(shipment.shipping_city)):
                    nb_local_products = nb_local_products + order.nb_products
                else:
                    nb_far_products = nb_far_products + order.nb_products
                
        return self.get_price_and_associated_rules(shipment.category, nb_local_products, nb_far_products)
            #self.get_price_and_associated_rules(shipment.category, shipment.shipping_city, shipment.nb_products)
            
    def get_price_and_associated_rules(self, category=Category_Enum.ARTICLE.value,  nb_local_products=0.0, nb_far_products=0):
        shipping_price = 0.0
        ret = 0.0
        rules = ''
        
        if self.is_article(category) and nb_local_products > 0 and nb_local_products < 7:
            ret = ret + self.local_shipping_price.get(int(nb_local_products)) 
            rules = rules + "article_local_"+str(nb_local_products) + " - "

        elif self.is_article(category) and nb_local_products >= 7:
            ret = ret + self.local_shipping_price.get(1) + (self.local_shipping_price.get('n') * int(nb_local_products-1))
            rules = rules + "article_local_"+str(nb_local_products) + " - "

        if self.is_article(category) and nb_far_products > 0  and nb_far_products < 6  and nb_local_products < 7:
            ret = ret + self.far_shipping_price.get(int(nb_far_products))
            rules = rules + "article_non-local_"+str(nb_far_products)
            
        elif self.is_article(category) and nb_far_products < 6  and nb_local_products  >= 7:
            ret = ret + self.far_shipping_price.get(1) + (self.far_shipping_price.get(
                'n') * int(nb_far_products-1))
            rules = rules + "article_local-et-non-local_"+str(nb_far_products)
        
        elif self.is_article(category) and nb_far_products >= 6:
            ret = self.far_shipping_price.get(1) + (self.far_shipping_price.get(
                'n') * int(nb_far_products-1)) 
            rules = "article_non-local_"+str(nb_far_products)

        if self.is_coursette(category) and nb_local_products > 0:
            ret, rules = self.local_shipping_price.get('c'), "coursette_local"

        elif self.is_coursette(category) and nb_far_products > 0:
            ret, rules = self.far_shipping_price.get(
                'c'), "coursette_non-local"

        if self.is_drive(category) and nb_local_products > 0:
            ret, rules = self.local_shipping_price.get('d'), "drive_local"

        elif self.is_drive(category) and nb_far_products > 0:
            ret, rules = self.far_shipping_price.get('d'), "drive_non-local"
        
        if ret == None:
            ret = 0.0
        return format(ret, '.2f'), rules


    # def get_price_and_associated_rules_sub(self, subscription):
       
    # def get_price_and_associated_rules(self, category, customer_city, seller_city, nb_products=0):
    #     if self.is_article(category) and self.is_from_local_area(customer_city) and self.is_from_local_area(seller_city) and nb_products < 7:
    #         ret, rules = self.local_shipping_price.get(int(nb_products)), "article_local_"+str(nb_products)

    #     elif self.is_article(category) and self.is_from_local_area(customer_city) and self.is_from_local_area(seller_city) and nb_products >= 7:
    #         ret, rules = self.local_shipping_price.get(
    #             1) + (self.local_shipping_price.get('n') * int(nb_products-1)), "article_local_"+str(nb_products)

    #     elif self.is_article(category) and (not self.is_from_local_area(customer_city) or not self.is_from_local_area(seller_city)) and nb_products < 6:
    #         ret, rules = self.far_shipping_price.get(
    #             int(nb_products)), "article_non-local_"+str(nb_products)

    #     elif self.is_article(category) and (not self.is_from_local_area(customer_city) or not self.is_from_local_area(seller_city)) and nb_products >= 6:
    #         ret, rules = self.far_shipping_price.get(1) + (self.far_shipping_price.get(
    #             'n') * int(nb_products-1)), "article_non-local_"+str(nb_products)

    #     elif self.is_coursette(category) and self.is_from_local_area(customer_city):
    #         ret, rules = self.local_shipping_price.get('c'), "coursette_local"

    #     elif self.is_coursette(category) and (not self.is_from_local_area(customer_city) or not self.is_from_local_area(seller_city)):
    #         ret, rules = self.far_shipping_price.get(
    #             'c'), "coursette_non-local"

    #     elif self.is_drive(category) and self.is_from_local_area(customer_city) and self.is_from_local_area(seller_city):
    #         ret, rules = self.local_shipping_price.get('d'), "drive_local"

    #     elif self.is_drive(category) and not self.is_from_local_area(customer_city) and self.is_from_local_area(seller_city):
    #         ret, rules = self.far_shipping_price.get('d'), "drive_non-local"
    #     if ret == None:
    #         ret = 0.0
    #     return format(ret, '.2f'), rules

