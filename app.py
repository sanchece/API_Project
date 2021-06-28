from flask import Flask,request,session, g, redirect,flash
from flask.templating import render_template
from requests.sessions import Session
from models import db, connect_db,User,Playlist,Song,Playlist_Songs
import requests
import json
from forms import AddUser, LoginUser, SavePlaylist
import os
import requests
from twitter_helper import get_tweets,get_id
from google_helper import google_sentiment_analysis,get_focus_sentiment
from spotify_helper import get_urmusic, get_danceability


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///urmusic')
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

connect_db(app)
# db.session.rollback()
# db.drop_all()
# # # # db.session.rollback()
# db.create_all()
# db.session.rollback()



USER_KEY="current_user"

@app.before_request
def add_user_to_g():
    if USER_KEY in session:
        g.user=User.query.get(session[USER_KEY])
    else:
        g.user=None

def login(user):
    session[USER_KEY]=user.id

def logout():
    if USER_KEY in session:
        del session[USER_KEY]


@app.route('/')
def home():
    if not g.user:
        return render_template("ur_music_home.html")
    else:
        user= User.query.get_or_404(session[USER_KEY])
        
        return redirect(f'/get_urmusic/{user.twitter_handle}')


@app.route('/signup', methods=["GET","POST"])
def signup():
    form=AddUser()
    if form.validate_on_submit():
        # sign up
        user=User.signup(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            twitter_handle=form.twitter_handle.data
        )
        db.session.commit()
        login(user)
        return redirect(f'/get_urmusic/{form.twitter_handle.data}')
    else:
        return render_template("signup_form.html",form=form)




@app.route('/save_playlist/<int:playlist_id>',methods=["POST"])
def save(playlist_id):
    form=SavePlaylist()
    if form.validate_on_submit():
        playlist_name=form.name.data
        playlist=Playlist.query.get_or_404(playlist_id)
        playlist.name=playlist_name
        user=User.query.get_or_404(playlist.user_id)
        db.session.add(playlist)
        db.session.commit()
        return redirect(f'/ur_profile/{user.id}')
    


@app.route('/login',methods=["GET","POST"])
def do_login():
    form=LoginUser()
    try:
        if form.validate_on_submit():
            user = User.authenticate(form.username.data,form.password.data)
            login(user)
            return redirect(f'/get_urmusic/{user.twitter_handle}')
    except:
        flash("Incorrect password or username")
        return redirect('/login')
    

    return render_template("login.html",form=form)






@app.route('/logout')
def do_logout():
    logout()
    return redirect('/')

@app.route('/get_urmusic/<string:username>', methods=["GET","POST"])
def urMusic(username):
    if not g.user:
        results="unauthorized"
        render_template('results.html',music=results)

    form=SavePlaylist()

    try:
        user_twitter_id=get_id(username)
        tweets=get_tweets(user_twitter_id)
        sentiments=[]
    
        for tweet in tweets:
            sentiment=google_sentiment_analysis(tweet['text'])
            sentiments.append(sentiment.score)
    
    
        focus_sentiment=round(get_focus_sentiment(sentiments),2)
    
        target_danceability=get_danceability(focus_sentiment)
        music= get_urmusic(focus_sentiment)
        new_playlist=Playlist(
            sentiment=focus_sentiment,
            danceability=target_danceability,
            user_id=session[USER_KEY]
        )
        db.session.add(new_playlist)
        db.session.commit()
        recommended_music=[]
        for track in music:
            artist=track['artists'][0]['name']
            image=track['album']['images'][0]['url']
            track_title=track['name']
            track_id=track['id']
    
            new_track=Song(
                artist=artist,
                title=track_title,
                spotify_id=track_id,
                spotify_image=image
            )
            db.session.add(new_track)
            db.session.commit()
            playlist_song_relationship=Playlist_Songs(
                playlist_id=new_playlist.id,
                song_id=new_track.id
            )
            db.session.add(playlist_song_relationship)
            db.session.commit()
            recommended_music.append([track_title,artist,image,track_id])
            user=User.query.get_or_404(session[USER_KEY])
    except:
        flash("Invalid Twitter handle")
        return redirect('/signup')

    return render_template('results.html',music=recommended_music,focus=focus_sentiment,
    user_id=user.id,username=username,playlist_id=new_playlist.id, form=form)


@app.route('/ur_profile/<string:user_id>', methods=["GET"])
def urProfile(user_id):
    user=User.query.get_or_404(user_id)
    users_playlists=Playlist.query.filter(Playlist.user_id==user.id).all()
    
    return render_template('profile.html',username=user.twitter_handle,user_id=user.id,playlists=users_playlists)

@app.route('/get_playlist/<int:playlist_id>')
def get_playlist(playlist_id):
    playlist_song_ids=Playlist_Songs.query.filter(Playlist_Songs.playlist_id==playlist_id)
    playlist_songs=[]
    for id in playlist_song_ids:
        song=Song.query.get_or_404(id.song_id)
        playlist_songs.append(song)
    user=User.query.get_or_404(session[USER_KEY])
    playlist=Playlist.query.get_or_404(playlist_id)
    return render_template('playlist.html',playlist_songs=playlist_songs,user=user,playlist=playlist)






