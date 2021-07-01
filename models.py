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
    username=db.Column(db.String,nullable=False,unique=True)
    password=db.Column(db.String,nullable=False)
    email=db.Column(db.String,nullable=False)
    twitter_handle=db.Column(db.String,nullable=False)


    playlists = db.relationship('Playlist', backref='users', cascade='all, delete')
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

    @classmethod
    def authenticate(cls, username, password):
        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False



class Playlist(db.Model):
    """playlists"""
    __tablename__="playlists"
    
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String,nullable=True,default="Not Named")
    sentiment=db.Column(db.String,nullable=False)
    danceability=db.Column(db.String,nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )

class Song(db.Model):
    """songs"""
    __tablename__="songs"
    
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    artist=db.Column(db.String,nullable=False)
    title=db.Column(db.String,nullable=False)
    spotify_id=db.Column(db.String)
    spotify_image=db.Column(db.String)

class Playlist_Songs(db.Model):
    __tablename__="playlistsongs"
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    playlist_id=db.Column(
        db.Integer,
        db.ForeignKey('playlists.id', ondelete='CASCADE')
    )
    song_id=db.Column(
        db.Integer,
        db.ForeignKey('songs.id', ondelete='CASCADE')
    )



