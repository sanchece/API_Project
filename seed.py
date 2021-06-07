from app import app
from models import db, connect_db,User,Playlist,Song,Playlist_Songs


db.drop_all()
db.create_all()
db.session.rollback()
user1=User.signup(
    username="grizzbear",
    email="grizzbear@gmail.com",
    password="password123",
    twitter_handle="CarlosS21109669"
)
db.session.commit()

playlist1=Playlist(
    sentiment=".5",
    danceability=".7",
    user_id=1
)
song1=Song(
    artist="tee grizzly",
    title="8 mile road"
)
db.session.add_all([playlist1,song1])
db.session.commit()
playlist_song1=Playlist_Songs(
    playlist_id=1,
    song_id=1
)
db.session.add(playlist_song1)
db.session.commit()