from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
db = SQLAlchemy()
bcrypt=Bcrypt()
def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """users"""
    __tablename__="users"
    
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String,nullable=False)
    password=db.Column(db.String,nullable=False)
    email=db.Column(db.String,nullable=False)
    twitter_handle=db.Column(db.String,nullable=False)

    @classmethod
    def signup(cls, username,email,password,twitter_handle):
        bcrypted_pw= bcrypt.generate_password_hash(password).decode('UTF-8')
        user=User(
            username=username,
            email=email,
            password=bcrypted_pw,
            twitter_handle=twitter_handle  
        )
        db.session.add(user)
        return user


class Playlist(db.Model):
    """playlist"""
    __tablename__="playlists"
    
    PlaylistID=db.Column(db.Integer,primary_key=True,autoincrement=True)
    Mood=db.Column(db.String,nullable=False)
    UserID=db.Column(db.String)

# class Songs(db.Model):
#     """songs"""
#     __tablename__="songs"

