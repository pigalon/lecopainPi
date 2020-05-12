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
    def test_products_show(self):

        product = db.session.query(Product).first()

        with app.test_client() as client:
            response = client.get(f'/products/{product.id}',
                                  content_type='html/text')
        self.assertEqual(response.status_code, 200)
        assert product.name in str(response.data)

    def test_products_edit(self):

        product = db.session.query(Product).first()
        product.name = 'updated_product'

        with app.test_client() as client:
            response = client.post(f'/products/update/{product.id}', data=dict(
                name=product.name,
                description=product.description,
                price=product.price,
                seller_id=product.seller_id,
                status=product.status), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        assert product.name in str(response.data)

    def test_products_create(self):
        name = 'new_product'
        seller = db.session.query(Seller).first()

        with app.test_client() as client:
            response = client.post(f'/products/new', data=dict(
                name=name,
                description='description',
                price=0.65,
                seller_id = seller.id,
                status="CREE"), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        assert name in str(response.data)

    def test_products_ask_delete(self):
        sentence = 'supprimer ce produit '
        product = db.session.query(Product).first()

        with app.test_client() as client:
            response = client.get(f'/products/delete/{product.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        assert sentence in str(response.data)

    def test_products_confirm_delete(self):
        product = db.session.query(Product).first()
        products_count = db.session.query(Product).count()

        with app.test_client() as client:
            response = client.delete(
                f'/products/{product.id}', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        assert products_count == (db.session.query(Product).count() + 1)


if __name__ == '__main__':
    unittest.main()
