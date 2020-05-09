from base import BaseTestCase
from lecopain.app import app, db
from lecopain.dao.models import User, Order, Seller
import os
import sys
import unittest
from flask_testing import TestCase, LiveServerTestCase
from flask_testing.utils import ContextVariableDoesNotExist


dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)


class FlaskTestCase(BaseTestCase, TestCase):

    # Ensure that Flask was set up correctly
    def test_orders_index(self):

        order = db.session.query(Order).first()

        # with app.test_client() as client:
        #     response = client.get(f'/orders/{order.id}',
        #                           content_type='html/text')
        # self.assertEqual(response.status_code, 200)
        # assert 'Commande client' in str(response.data)
        # assert order.id in str(response.data)


if __name__ == '__main__':
    unittest.main()
