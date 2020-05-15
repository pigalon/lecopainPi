from lecopain.tests.base import BaseTestCase
from lecopain.app import app, db
from lecopain.services.order_manager import OrderManager
import unittest
from flask_testing import TestCase




class OrdermanagerTestCase(BaseTestCase, TestCase):

    # Ensure that Flask was set up correctly
    def test_order_status(self):

        orderServices = OrderManager()
        
        for status in orderServices.get_order_status():
            print(f'status : {status}')


if __name__ == '__main__':
    unittest.main()
