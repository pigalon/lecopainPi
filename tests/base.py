from lecopain.dao.models import User, Customer, Order, Product
from lecopain.app import app, db
import unittest
import sys
import os
from factories import AdminFactory, ProductFactory, CustomerFactory, OrderFactory


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
        self.create_orders()

        order = Order.query.first()
        product = Product.query.first()
        order.add_products([(product, 6, 2)])
        db.session.commit()

        print("!!!!!order :" + str(order.id))

        for product in order.products:
            print("!!!!!product :" + str(vars(product)))

        for line in order.lines:
            print("!!!!!line :" + str(vars(line)))

        # self.create_order_2products()

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

    def create_products(self):
        ProductFactory.create(name='product1', price=1.00)
        ProductFactory.create(name='product2', price=2.00)
        ProductFactory.create(name='product3', price=3.00)

    def create_customers(self):
        CustomerFactory.create()
        CustomerFactory.create()

    def create_orders(self):
        OrderFactory.create()

    # def create_order_2products(self):
    #     OrderWith2ProductsFactory.create()
