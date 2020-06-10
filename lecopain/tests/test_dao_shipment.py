from lecopain.tests.base import BaseTestCase
from lecopain.app import app, db
from lecopain.dao.models import Shipment
from lecopain.dao.shipment_dao import ShipmentDao
import os
import sys
import unittest
from flask_testing import TestCase


dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)


class ShipmentDAOTestCase(BaseTestCase, TestCase):

    # Ensure that Flask was set up correctly
    def test_read_one(self):

        shipment = db.session.query(Shipment).first()

        shipment_result = ShipmentDao.read_one(shipment.id)

        assert shipment.title in str(shipment_result)


if __name__ == '__main__':
    unittest.main()
