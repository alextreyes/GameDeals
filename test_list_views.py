"""Test the models of the app"""

import os 
from unittest import TestCase

from models import db, connect_db, User, UserList, UserListGame, Likes

os.environ['DATABASE_URL'] = 'postgresql:///gamedeals-test'

from app import app, CURR_USER_KEY, g

db.drop_all()
db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class ListViewTestCase(TestCase):
    """Test case for lists views"""

    def setUp(self):
        """Set up test data and client"""
        # Delete existing records from the database
        UserListGame.query.delete()
        UserList.query.delete()
        User.query.delete()
        

        # Create a test client and app context
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Create a user record and add it to the session
        self.testuser = User.signup(username="alextreyes", password="123123")
        db.session.commit()
       

    def test_create_list(self):
        """Test creating a new list"""

        # Simulate a logged-in user
        with self.client as c:
            with c.session_transaction() as sess:
                # Set the current user in the session
                sess[CURR_USER_KEY] = self.testuser.id

            # Send a POST request to create a new list
            resp = c.post("/lists/new", data={"list_name": "Test List"})

            # Check if the request redirects to the lists page
            self.assertEqual(resp.status_code, 302, msg="Failed to redirect after creating a list")
            self.assertEqual(resp.location, "http://localhost/lists", msg="Incorrect redirect URL")

            # Check if the new list is added to the database
            new_list = UserList.query.filter_by(list_name="Test List", user_id=self.testuser.id).first()
            self.assertIsNotNone(new_list, msg="List not added to the database")
    
    def test_delete_list(self):
        """test deleting list"""
        l = UserList(id=1, list_name="test", user_id=self.testuser.id)
        db.session.add(l)
        db.session.commit()   

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.post("/lists/1/delete", follow_redirects=True)
            self.assertEqual(resp.status_code, 200)

            l = UserList.query.get(1)
            self.assertIsNone(l)

    def test_add_game(self):
        """Test adding a game to a list"""
        # Create a user list
        user_list = UserList(list_name="test", user_id=self.testuser.id)
        db.session.add(user_list)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                # Set the current user in the session
                sess[CURR_USER_KEY] = self.testuser.id

            # Send a POST request to add the game to the list
            resp = c.post("/lists/add_game", data={"game_id": "1", "list_id": "1", "title":"Test Game"})
            self.assertEqual(resp.status_code, 302)

            # Check if the game is added to the database
            added_game = UserListGame.query.filter_by(name="Test Game").first()
            self.assertIsNotNone(added_game)

    def test_delete_game(self):
        """Test deleting a game from a list"""

        # Create and add a user list to the database
        user_list = UserList(id=1, list_name="test", user_id=self.testuser.id)
        db.session.add(user_list)
        db.session.commit()

        # Create and add a game to the user list
        game = UserListGame(game_id=1, list_id=1, name="Test Game")
        db.session.add(game)
        db.session.commit()

        with self.client as c:
            with c.session_transaction() as sess:
                # Set the current user in the session
                sess[CURR_USER_KEY] = self.testuser.id
            
            resp = c.post(f"/lists/{1}/remove_game", data={"list_id": 1, "game_id":"1"})
            self.assertEqual(resp.status_code, 302)
















            


