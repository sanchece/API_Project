from flask import Flask,request,session, g, redirect
from flask.templating import render_template
from requests.sessions import Session
from models import db, connect_db,User,Playlist,Song,Playlist_Songs
import requests
import json
from forms import AddUser, LoginUser
import os
import requests
from twitter_helper import get_tweets,get_id
from google_helper import google_sentiment_analysis,get_focus_sentiment
from spotify_helper import get_urmusic, get_danceability


app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///urmusic')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("://", "ql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

connect_db(app)

# db.drop_all()
# db.create_all()


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

@app.route('/login',methods=["GET","POST"])
def do_login():
    form=LoginUser()
    if form.validate_on_submit():
        user = User.authenticate(form.username.data,form.password.data)
        login(user)
        return redirect(f'/get_urmusic/{user.twitter_handle}')
    

    return render_template("login.html",form=form)


@app.route('/logout')
def do_logout():
    logout()
    return redirect('/')

@app.route('/get_urmusic/<string:username>', methods=["GET","POST"])
def urMusic(username):

    # return render_template('results.html',music="music")
    if not g.user:
        results="unauthorized"
        render_template('results.html',music=results)
    user_id=get_id(username)

    tweets=get_tweets(user_id)
    # return f"{tweets}"
    sentiments=[]

    for tweet in tweets:
        sentiment=google_sentiment_analysis(tweet['text'])
        # sentiments.append(sentiment)
        sentiments.append(sentiment.score)


    # return f"{sentiments}"
    focus_sentiment=round(get_focus_sentiment(sentiments),2)
    # return f'{[focus_sentiment,sentiments]}'

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
        track=track['name']
        
        # ['images'][0]['url']
        new_track=Song(
            artist=artist,
            title=track
        )
        db.session.add(new_track)
        db.session.commit()
        playlist_song_relationship=Playlist_Songs(
            playlist_id=new_playlist.id,
            song_id=new_track.id
        )
        db.session.add(playlist_song_relationship)
        db.session.commit()
        recommended_music.append([track,artist,image])

    return render_template('results.html',music=recommended_music,focus=focus_sentiment,username=username)









