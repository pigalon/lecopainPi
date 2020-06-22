from lecopain.dao.models import Category_Enum
from lecopain.dao.models import OrderStatus_Enum
class BusinessService:
    local_shipping_price = {1:0.6, 2:1.16, 3:1.62, 4:2.05, 5:2.20, 6:2.70, 'n':0.40, 'c':5, 'd':8}
    far_shipping_price = {1: 0.65, 2: 1.25,
                          3: 1.75, 4: 2.20, 5: 2.50, 'n': 0.45, 'c': 6, 'd': 8}
    coursette = {'langlade': 5.0, '!langlade': 6.0}
    course = {'langlade': 12.0, '!langlade': 12.0}
    drive = {'langlade': 8.0, '!langlade': 8.0}
    petitou = {'langlade': 5.0, 
                      'nages':6,
                      'stDionisy':6, 
                      'clarensac':7,
                      'caveirac':7,
                      'calvisson':8,
                      'bizac':8, 
                      'boissières':8} 
                      
    def is_from_local_area(self, city):
        return city.lower() == 'langlade'
    
    def is_from_foreign_area(self, city):
        return city.lower() != 'langlade'
    
    def is_from_clarensac_area(self, city):
        return city.lower() == 'clarensac'
    
    def is_from_stdionisy_area(self, city):
        return city.lower() == 'stdionisy'
    
    def is_from_nages_area(self, city):
        return city.lower() == 'nages et solorgues'
    
    def is_from_caveirac_area(self, city):
        return city.lower() == 'caveirac'
    
    def is_from_calvisson_area(self, city):
        return city.lower() == 'calvisson'
    
    def is_from_bizac_area(self, city):
        return city.lower() == 'bizac'
    
    def is_from_boissieres_area(self, city):
        return city.lower() == 'boissières'

    def is_article(self, category):
        return category == Category_Enum.ARTICLE.value

    def is_coursette(self, category):
        return category == Category_Enum.COURSETTE.value

    def is_course(self, category):
        return category == Category_Enum.COURSE.value

    def is_drive(self, category):
        return category == Category_Enum.DRIVE.value
    
    def is_petitou(self, category):
        return category == Category_Enum.PETITOU.value

    # def apply_rules_just_order(self, order):
    #     return self.get_price_and_associated_rules(order.shipment.category, order.shipment.shipping_city, order.seller.city, order.nb_products)
    
    def get_all_products_numbers(self, subscription_day):
        nb_local_products = 0
        nb_far_products = 0
        
        for line in subscription_day.lines:
            if self.is_from_local_area(line.product.seller.city) and self.is_from_local_area(subscription_day.subscription.customer.city):
                nb_local_products = nb_local_products + line.quantity
            else :
                nb_far_products = nb_far_products + line.quantity
        return nb_local_products, nb_far_products

    def apply_rules_for_subscription_day(self, subscription_day):
        amount = 0.0
        nb_local_products = 0
        nb_far_products = 0

        nb_local_products, nb_far_products = self.get_all_products_numbers(subscription_day)
                
        return self.get_price_and_associated_rules(subscription_day.subscription.category, nb_local_products, nb_far_products)

    def apply_rules_for_shipment(self, shipment):
        amount = 0.0
        nb_local_products = 0
        nb_far_products = 0
        city=''
                
        for order in shipment.orders:
            if order.status != OrderStatus_Enum.ANNULEE.value:
                if(self.is_from_local_area(order.seller.city) and self.is_from_local_area(shipment.shipping_city)):
                    nb_local_products = nb_local_products + order.nb_products
                else:
                    nb_far_products = nb_far_products + order.nb_products
        
        if self.is_petitou(shipment.category):
            city = shipment.shipping_city.lower()
        
        return self.get_price_and_associated_rules(shipment.category, nb_local_products, nb_far_products, city)
            #self.get_price_and_associated_rules(shipment.category, shipment.shipping_city, shipment.nb_products)
            
    def get_price_and_associated_rules(self, category=Category_Enum.ARTICLE.value,  nb_local_products=0.0, nb_far_products=0, city=''):
        shipping_price = 0.0
        ret = 0.0
        rules = ''
        
        if self.is_article(category) and nb_local_products > 0 and nb_local_products < 6:
            ret = ret + self.local_shipping_price.get(int(nb_local_products)) 
            rules = rules + "article_local_"+str(nb_local_products) + " - "

        elif self.is_article(category) and nb_local_products >= 6:
            ret = ret + self.local_shipping_price.get(1) + (self.local_shipping_price.get('n') * int(nb_local_products-1))
            rules = rules + "article_local_"+str(nb_local_products) + " - "

        if self.is_article(category) and nb_far_products > 0  and nb_far_products < 6  and nb_local_products < 6:
            ret = ret + self.far_shipping_price.get(int(nb_far_products))
            rules = rules + "article_non-local_"+str(nb_far_products)
            
        elif self.is_article(category) and nb_far_products > 0 and nb_far_products < 6  and nb_local_products  >= 6:
            ret = ret + self.far_shipping_price.get(1) + (self.far_shipping_price.get(
                'n') * int(nb_far_products-1))
            rules = rules + "article_local-et-non-local_"+str(nb_far_products)
        
        elif self.is_article(category) and nb_far_products >= 6:
            ret = self.far_shipping_price.get(1) + (self.far_shipping_price.get(
                'n') * int(nb_far_products-1)) 
            rules = "article_non-local_"+str(nb_far_products)

        if self.is_coursette(category) and nb_local_products > 0:
            ret, rules = self.coursette.get('langlade'), "coursette_local" #.local_shipping_price.get('c'), "coursette_local"

        elif self.is_coursette(category) and nb_far_products > 0:
            ret, rules = self.coursette.get('!langlade'), "coursette_non-local"

        if self.is_drive(category) and nb_local_products > 0:
            ret, rules = self.drive.get('langlade'), "drive_local"
            
        elif self.is_drive(category) and nb_far_products > 0:
            ret, rules = self.drive.get('!langlade'), "drive_non-local"
        
        if self.is_course(category) and nb_local_products > 0:
            ret, rules = self.course.get('langlade'), "drive_local"
            
        elif self.is_course(category) and nb_far_products > 0:
            ret, rules = self.course.get('!langlade'), "drive_non-local"
            
        if self.is_petitou(category) and self.is_from_local_area(city):
            ret, rules = self.petitou.get('langlade'), "petitou_local"
            
        elif self.is_petitou(category) and self.is_from_nages_area(city):
            ret, rules = self.petitou.get('nages'), "petitou-nages"
        
        elif self.is_petitou(category) and self.is_from_clarensac_area(city):
            ret, rules = self.petitou.get('clarensac'), "petitou-clarensac"
        
        elif self.is_petitou(category) and self.is_from_caveirac_area(city):
            ret, rules = self.petitou.get('caveirac'), "petitou-caveirac"
        
        elif self.is_petitou(category) and self.is_from_stdionisy_area(city):
            ret, rules = self.petitou.get('stdionisy'), "petitou_stdionisy"
        
        elif self.is_petitou(category) and self.is_from_bizac_area(city):
            ret, rules = self.petitou.get('bizac'), "petitou_bizac"
        
        elif self.is_petitou(category) and self.is_from_calvisson_area(city):
            ret, rules = self.petitou.get('calvisson'), "petitou_bizac"

        
        if ret == None:
            ret = 0.0
        return format(ret, '.2f'), rules


