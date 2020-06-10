from lecopain.dao.models import User, Customer, Order, Product, Line
from lecopain.app import app, db
import unittest
import sys
import os
from lecopain.tests.factories import (AdminFactory,
    ProductFactory,
    CustomerFactory,
    OrderFactory,
    SellerFactory,
    ShipmentFactory)


dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)


class BaseTestCase(unittest.TestCase):
    """A base test case."""

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        self.app = self.create_app()
        db.create_all()

        self.create_users()
        self.create_products()
        self.create_customers()
        self.create_shipments()
        self.create_orders()
        self.create_sellers()

        #order = Order.query.first()
        product = Product.query.first()
        #order.add_products([(product, 6, 2)])
        #line = Line(order=order,product_id=product.id,quantity=2,price=1.00)
        #order.add_line(line)

        db.session.commit()

    def login(self, username, password):
        return self.client.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.get_engine(self.app).dispose()

    def create_users(self):
        AdminFactory.create()
        
    def create_sellers(self):
        SellerFactory.create()

    def create_products(self):
        ProductFactory.create(name='product1', price=1.00)
        ProductFactory.create(name='product2', price=2.00)
        ProductFactory.create(name='product3', price=3.00)

    def create_customers(self):
        CustomerFactory.create()
        CustomerFactory.create()

    def create_orders(self):
        OrderFactory.create()
        
    def create_shipments(self):
        ShipmentFactory.create()
        print("shipment created")

