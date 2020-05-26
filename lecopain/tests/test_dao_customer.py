from lecopain.tests.base import BaseTestCase
from lecopain.app import app, db
from lecopain.dao.models import Customer
from lecopain.dao.customer_dao import CustomerDao
import os
import sys
import unittest
from flask_testing import TestCase


dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)


class CustomerDAOTestCase(BaseTestCase, TestCase):

    # Ensure that Flask was set up correctly
    def test_get_all_cities(self):

        cities = CustomerDao.get_all_cities()

        print(f'cities : {cities}')
        assert len(cities) > 0

    def test_read_all_by_city(self):
        customer = Customer.query.first()
        customers = CustomerDao.read_all_by_cities(customer.city)

        print(f'customers : {customers}')
        assert len(customers) > 0

if __name__ == '__main__':
    unittest.main()
