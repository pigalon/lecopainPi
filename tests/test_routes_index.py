from base import BaseTestCase
from lecopain import app
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
    def test_index(self):
        with app.test_client() as client:
            response = client.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    def test_index_login(self):
        page = self.login('admin', 'password')
        assert 'home' in str(page.data)

    def test_products_index(self):
        with app.test_client() as client:
            response = client.get('/products', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        assert 'les produits' in str(response.data)

    def test_vendors_index(self):
        with app.test_client() as client:
            response = client.get('/vendors', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        assert 'Vendeurs' in str(response.data)

    def test_customers_index(self):
        with app.test_client() as client:
            response = client.get('/customers', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        assert 'Clients' in str(response.data)

    def test_orders_index(self):
        with app.test_client() as client:
            response = client.get('/orders', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        assert 'Toutes les commandes' in str(response.data)

    def test_deliveries_index(self):
        with app.test_client() as client:
            response = client.get('/deliveries', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        assert 'Les livraisons' in str(response.data)

    def test_customers_index(self):
        with app.test_client() as client:
            response = client.get('/customers', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        assert 'Clients' in str(response.data)


if __name__ == '__main__':
    unittest.main()
