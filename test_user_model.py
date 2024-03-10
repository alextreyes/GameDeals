"""Test the user model"""

import os 
from unittest import TestCase

from models import db, connect_db, User, UserList, UserListGame, Likes

os.environ['DATABASE_URL'] = 'postgresql:///gamedeals-test'

from app import app, CURR_USER_KEY, g

db.drop_all()
db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class UserModelTestCase(TestCase):
    """test user model"""
    
    def setUp(self):
        """Set up test data and client"""
        User.query.delete()

        self.client = app.test_client()
        app.config['TESTING'] = True   
    
    def test_user_model(self):
        """basic functions of the model"""

        u = User(id = 1,
                 username="test",
                 password="TEST")
        
        db.session.add(u)
        db.session.commit()

        test = User.query.filter_by(username="test").first()
        
        self.assertIsNotNone(test)
        self.assertEqual(test.username,"test")
    
    def test_user_signup(self):
        """test signup"""

        a = User.signup(username="test123", password="TEST")
        db.session.commit()

        self.assertIsInstance(a,User)
    
    def test_authenticate(self):
        """test authenticate"""

        u1 = User.signup(username="testuser1", password="HASHED_PASSWORD")
        db.session.commit()

        self.assertIs(User.authenticate(username='testuser1', password='HASHED_PASSWORD'), u1)

        self.assertIs(User.authenticate(username='testuser1', password='HASHED_PASS'), False)

        self.assertIs(User.authenticate(username='test', password='HASHED_PASS'), False)
