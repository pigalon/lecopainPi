from lecopain.tests.base import BaseTestCase
from lecopain.app import app, db
from lecopain.dao.models import User, Customer, Seller
import os
import sys
import unittest
from flask_testing import TestCase, LiveServerTestCase
from flask_testing.utils import ContextVariableDoesNotExist


dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)


class CustomerTestCase(BaseTestCase, TestCase):

    # Ensure that Flask was set up correctly
    def test_customers_show(self):

        customer = db.session.query(Customer).first()

        with app.test_client() as client:
            response = client.get(f'/customers/{customer.id}',
                                  content_type='html/text')
        self.assertEqual(response.status_code, 200)
        assert 'client' in str(response.data)
        assert str(customer.id) in str(response.data)


if __name__ == '__main__':
    unittest.main()
