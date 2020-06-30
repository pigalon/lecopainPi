from lecopain.tests.base import BaseTestCase
from lecopain.app import app, db
from lecopain.dao.models import User
import os
import sys
import unittest
from flask_testing import TestCase


dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)


class TestUserCase(BaseTestCase, TestCase):

    # Ensure that Flask was set up correctly
    def test_user_details(self):
        user = User.query.first()

        print(f'user : {user}')
        
        print(f'is active  : {user.active}')
        if user.is_active():
            print('active is True')
        else:
            print('active is False')
        print(f'is authenticated  : {user.is_authenticated}')
        print(f'is anonymous  : {user.is_anonymous}')
        
        user = User(username='toto', email='test', password='pass')
        
        print(f'user : {user}')
        
        print(f'is ative  : {user.active}')
        print(f'is authenticated  : {user.is_authenticated}')
        print(f'is anonymous  : {user.is_anonymous}')
        
    
if __name__ == '__main__':
    unittest.main()
