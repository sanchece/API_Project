from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """users"""
    __tablename__="users"
    
    UserID=db.Column(db.Integer,primary_key=True,autoincrement=True)
    Name=db.Column(db.String,nullable=False)
    Email=db.Column(db.String,nullable=False)
    Twitter_handle=db.Column(db.String,nullable=False)

class Playlist(db.Model):
    """playlist"""
    __tablename__="playlists"
    
    PlaylistID=db.Column(db.Integer,primary_key=True,autoincrement=True)
    Mood=db.Column(db.String,nullable=False)
    UserID=db.Column(db.String)

# class Songs(db.Model):
#     """songs"""
#     __tablename__="songs"

