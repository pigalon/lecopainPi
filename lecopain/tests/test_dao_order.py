from lecopain.tests.base import BaseTestCase
from lecopain.app import app, db
from lecopain.dao.models import Order
from lecopain.dao.order_dao import OrderDao
import os
import sys
import unittest
from flask_testing import TestCase


dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)


class OrderDAOTestCase(BaseTestCase, TestCase):

    # Ensure that Flask was set up correctly
    def test_read_one(self):
        order = db.session.query(Order).first()
        order_result = OrderDao.read_one(order.id)
        assert order.title in str(order_result)


if __name__ == '__main__':
    unittest.main()
