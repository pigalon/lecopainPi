from lecopain.tests.base import BaseTestCase
from lecopain.app import app, db
from lecopain.services.business_service import BusinessService
from lecopain.dao.models import Category_Enum
import unittest
from flask_testing import TestCase




class BusinessServiceTestCase(BaseTestCase, TestCase):
    def test_article_local_less_seven(self):
        pass
    # Ensure that Flask was set up correctly
    # def test_article_local_less_seven(self):
    #     businessService = BusinessService()
    #     price, rules = businessService.get_price_and_associated_rules(
    #         category=Category_Enum.ARTICLE.value, city='Langlade', nb_products=1)
    #     assert float(price) == 0.60
    # def test_article_local_equal_seven(self):
    #     businessService = BusinessService()
    #     price, rules = businessService.get_price_and_associated_rules(
    #         category=Category_Enum.ARTICLE.value, city='Langlade', nb_products=7)
    #     assert float(price) == 3.00
    # def test_article_far_less_six(self):
    #     businessService = BusinessService()
    #     price, rules = businessService.get_price_and_associated_rules(
    #         category=Category_Enum.ARTICLE.value, city='Nimes', nb_products=1)
    #     assert float(price) == 0.65
    # def test_article_far_equal_six(self):
    #     businessService = BusinessService()
    #     price, rules = businessService.get_price_and_associated_rules(
    #         category=Category_Enum.ARTICLE.value, city='Nimes', nb_products=6)
    #     assert float(price) == 2.90
    # def test_coursette_local(self):
    #     businessService = BusinessService()
    #     price, rules = businessService.get_price_and_associated_rules(
    #         category=Category_Enum.COURSETTE.value, city='Langlade')
    #     assert float(price) == 5.0

    # def test_coursette_far(self):
    #     businessService = BusinessService()
    #     price, rules = businessService.get_price_and_associated_rules(
    #         category=Category_Enum.COURSETTE.value, city='Nimes')
    #     assert float(price) == 6.0

    # def test_drive_local(self):
    #     businessService = BusinessService()
    #     price, rules = businessService.get_price_and_associated_rules(
    #         category=Category_Enum.DRIVE.value, city='Langlade')
    #     assert float(price) == 8.0

    # def test_drive_far(self):
    #     businessService = BusinessService()
    #     price, rules = businessService.get_price_and_associated_rules(
    #         category=Category_Enum.DRIVE.value, city='Nimes')
    #     assert float(price) == 8.00



if __name__ == '__main__':
    unittest.main()
