import os
from unittest import TestCase
from models import db, connect_db, User, Playlist, Song, Playlist_Songs
from app import app, USER_KEY

os.environ['DATABASE_URL']="postgresql:///warbler"
app.config['WTF_CSRF_ENABLED']=False

class UserModelTestCase(TestCase):

    def setUp(self):
        db.drop_all()
        db.create_all()

        self.grizzly=User.signup(
            username="grizzly",
            email="grizzly@hotmail.com",
            password="secret",
            twitter_handle="CarlosS21109669"
        )
        self.grizzly_id=300
        self.grizzly.id=self.grizzly_id
        db.session.commit()

        self.grizzly = User.query.get(self.grizzly_id)
        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_Song_model(self):
        self.test_song_1=Song(
            id=350,
            artist="grizzly",
            title="the forest",
            spotify_id="some_spotify_id",
            spotify_image="some_grizly_image.png"
            )
        db.session.add(self.test_song_1)
        db.session.commit()
        self.assertEqual(self.test_song_1.id, 350)
        self.assertEqual(self.test_song_1.artist, "grizzly")
        self.assertEqual(self.test_song_1.title,"the forest")

    def test_Playlist_model(self):
        self.test_playlist_1=Playlist(
            id=355,
            name="The songs of Grizzly",
            sentiment=0.7,
            danceability=0.85,
            user_id=self.grizzly_id
            )
        db.session.add(self.test_playlist_1)
        db.session.commit()
        self.assertEqual(self.test_playlist_1.id, 355)
        self.assertEqual(self.test_playlist_1.name, "The songs of Grizzly")
        self.assertEqual(self.test_playlist_1.user_id,self.grizzly_id)

    def test_Playlist_songs_model(self):
        self.test_playlist_1=Playlist(
            id=355,
            name="The songs of Grizzly",
            sentiment=0.7,
            danceability=0.85,
            user_id=self.grizzly_id
            )
        db.session.add(self.test_playlist_1)
        db.session.commit()
        self.assertEqual(self.test_playlist_1.id, 355)
        self.assertEqual(self.test_playlist_1.name, "The songs of Grizzly")
        self.assertEqual(self.test_playlist_1.user_id,self.grizzly_id)
        self.test_song_1=Song(
            id=350,
            artist="grizzly",
            title="the forest",
            spotify_id="some_spotify_id",
            spotify_image="some_grizly_image.png"
            )
        db.session.add(self.test_song_1)
        db.session.commit()
        self.assertEqual(self.test_song_1.id, 350)
        self.assertEqual(self.test_song_1.artist, "grizzly")
        self.assertEqual(self.test_song_1.title,"the forest")

        self.test_playlist_songs_1=Playlist_Songs(
            id=360,
            playlist_id=355,
            song_id=350
            )
        db.session.add(self.test_playlist_songs_1)
        db.session.commit()
        self.assertEqual(self.test_playlist_songs_1.id, 360)
        self.assertEqual(self.test_playlist_songs_1.playlist_id, self.test_playlist_1.id)
        self.assertEqual(self.test_playlist_songs_1.song_id,self.test_song_1.id)
