from lecopain.tests.base import BaseTestCase
from lecopain.app import app, db
import unittest
from flask_testing import TestCase
from lecopain.dao.models import Line, Order, Product




class ModelTestCase(BaseTestCase, TestCase):

    # Ensure that Flask was set up correctly
    def test_line_building(self):
        
        order = Order.query.first()
        product = Product.query.first()
        #order.add_products([(product, 6, 2)])
        line = Line(order=order,product_id=product.id,quantity=2,price=1.00, specifications="bien cuit, coupé")
        order.add_line(line)
        db.session.commit()

        line = db.session.query(Line).first()
        print("line : " + str(line.specifications))

if __name__ == '__main__':
    unittest.main()
