from base import BaseTestCase
from lecopain.app import app, db
from lecopain.dao.models import User, Product, Seller
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
    def test_products_index(self):

        product = db.session.query(Product).first()

        with app.test_client() as client:
            response = client.get(f'/products/{product.id}',
                                  content_type='html/text')
        self.assertEqual(response.status_code, 200)
        assert product.name in str(response.data)


if __name__ == '__main__':
    unittest.main()
