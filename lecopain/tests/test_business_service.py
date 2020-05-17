from lecopain.tests.base import BaseTestCase
from lecopain.app import app, db
from lecopain.services.business_service import BusinessService
from lecopain.dao.models import ProductCategory_Enum
import unittest
from flask_testing import TestCase




class BusinessServiceTestCase(BaseTestCase, TestCase):
    
    

    # Ensure that Flask was set up correctly
    def test_article_local_inf_seven(self):
        businessService = BusinessService()
        price, rules = businessService.get_price_and_associated_rules(
            category=ProductCategory_Enum.ARTICLE.value, city='Langlade', nb_products=1)
        print(f'price : {price} - rules : {rules}')


if __name__ == '__main__':
    unittest.main()
