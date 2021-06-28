import os
from unittest import TestCase
from models import db, connect_db, User, Playlist, Song, Playlist_Songs
from app import app, USER_KEY

os.environ['DATABASE_URL']="postgresql:///warbler"
app.config['WTF_CSRF_ENABLED']=False

class MessageViewTestCase(TestCase):

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()
        self.client = app.test_client()

        self.grizzly=User.signup(
            username="grizzly",
            email="grizzly@hotmail.com",
            password="secret",
            twitter_handle="CarlosS21109669"
        )
        self.grizzly_id=300
        self.grizzly.id=self.grizzly_id
        db.session.commit()
    def tearDown(self):
        response = super().tearDown()
        db.session.rollback()
        return response
    def test_login(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[USER_KEY] = self.grizzly_id
            res= c.get("/",follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("this is Ur Music",str(res.data))

    def test_logout(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[USER_KEY] = self.grizzly_id
            res= c.get("/logout",follow_redirects=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn("Hello World",str(res.data))