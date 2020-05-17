from lecopain.dao.models import ProductCategory_Enum
class BusinessService:
    
    local_shipping_price = {1:0.6, 2:1.16, 3:1.62, 4:2.05, 5:2.20, 6:2.70, 'n':0.40, 'c':5, 'd':8}
    far_shipping_price = {1: 0.65, 2: 1.25,
                          3: 1.75, 4: 2.20, 5: 2.50, 'n': 0.40, 'c': 6, 'd': 8}

    def is_from_local_area(self, city):
        return city.lower() == 'langlade'

    def is_article(self, category):
        return category == ProductCategory_Enum.ARTICLE.value

    def is_coursette(self, category):
        return category == ProductCategory_Enum.COURSETTE.value

    def is_drive(self, category):
        return category == ProductCategory_Enum.DRIVE.value

    def get_price_and_associated_rules(self, category, city, nb_products):
        if self.is_article(category) and self.is_from_local_area(city) and nb_products < 7:
            return self.local_shipping_price.get(int(nb_products)), "article_local_"+str(nb_products)
        
        elif self.is_article(category) and self.is_from_local_area(city) and nb_products >= 7:
            return self.local_shipping_price.get(1) + (self.local_shipping_price.get('n') * int(nb_products)), "article_local_"+str(nb_products)
        
        elif self.is_article(category) and not self.is_from_local_area(city) and nb_products < 6:
            return self.far_shipping_price.get(int(nb_products)), "article_non-local_"+str(nb_products)
        
        elif self.is_article(category) and not self.is_from_local_area(city) and nb_products >= 6:
            return self.far_shipping_price.get(1) + (self.far_shipping_price.get('n') * int(nb_products)), "article_non-local_"+str(nb_products)
        
        elif self.is_coursette(category) and self.is_from_local_area(city):
            return self.local_shipping_price.get('c'), "coursette_local"
        
        elif self.is_coursette(category) and not self.is_from_local_area(city):
            return self.far_shipping_price.get('c'), "coursette_non-local"
        
        elif self.is_drive(category) and self.is_from_local_area(city):
            return self.local_shipping_price.get('d'), "drive_local"
        
        elif self.is_drive(category) and not self.is_from_local_area(city):
            return self.far_shipping_price.get('d'), "drive_non-local"

