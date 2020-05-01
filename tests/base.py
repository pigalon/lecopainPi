import unittest 
import sys, os


dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

from lecopain import app, db
from lecopain.dao.models import User


class BaseTestCase(unittest.TestCase): 
    """A base test case."""

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):
        app.config.from_object('config.TestConfig')
        db.create_all()
        db.session.add(User(username="admin", email="ad@min.com", password="admin"))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()