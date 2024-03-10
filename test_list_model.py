"""Test the list model"""

import os 
from unittest import TestCase

from models import db, connect_db, User, UserList, UserListGame, Likes

os.environ['DATABASE_URL'] = 'postgresql:///gamedeals-test'

from app import app, CURR_USER_KEY, g

db.drop_all()
db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class ListModelTestCase(TestCase):
    """Test case for lists model"""

    def setUp(self):
        """Set up test data and client"""
        UserList.query.delete()
        User.query.delete()
        

        # Create a test client and app context
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Create a user record and add it to the session
        self.testuser = User.signup( username="alextreyes", password="123123")
        db.session.commit()

    def test_list_model(self):
        """Testing basic model"""

        # Create and add a UserList instance to the database
        user_list = UserList(list_name="test", user_id=1)
        db.session.add(user_list)
        db.session.commit()

        # Retrieve the UserList instance from the database
        retrieved_list = UserList.query.filter_by(list_name="test").first()

        # Check if the retrieved UserList instance has the correct attributes
        self.assertIsNotNone(retrieved_list)  # Check if an instance is retrieved
        self.assertEqual(retrieved_list.list_name, "test")  # Check if list_name attribute is correct
