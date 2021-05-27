from flask import Flask,request
from flask.templating import render_template
from models import db, connect_db
import requests
import json
from statistics import mean
from google.cloud import language_v1
import base64
import requests
# for spotify below
clientId = ''
clientSecret = ''
# for twitter below
twitter_bearer_token=""

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///urmusic'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
# db.drop_all()
# db.create_all()






# def google_sentiment_analysis(tweet):
#     text=tweet
#     client = language_v1.LanguageServiceClient()
#     document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
#     sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment
#     return sentiment

# def get_focus_sentiment(sentiments):
#     # currently working on better algorithm to extract focus sentiment from extracted tweets
#     focus_sentiment=mean(sentiments)
#     return sentiments

# def get_token_for_spotify():
#     url="https://accounts.spotify.com/api/token"
#     auth_str ='{}:{}'.format(clientId, clientSecret)

#     headers={
#         "Content-Type":"application/x-www-form-urlencoded",
#         "Authorization":"Basic "+base64.urlsafe_b64encode(auth_str.encode()).decode(),
#         }
#     data={
#         'grant_type': 'client_credentials'
#         }

#     result=requests.post(url,data=data, headers=headers)
#     token=result.json()
#     return token['access_token']

# def get_random_song(playlist_id):
#     token= get_token_for_spotify()
#     params={"market":"US","limit":1}
#     headers={
#         "Authorization":"Bearer {}".format(token)
#     }
#     url=f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
#     response= requests.request("GET",url,headers=headers,params=params)
#     song=response.json()
#     return song["items"][0]["track"]["id"]


# def get_random_artist(playlist_id):
#     token= get_token_for_spotify()

#     params={"market":"US","limit":2}
#     headers={
#         "Authorization":"Bearer {}".format(token)
#     }
#     url=f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
#     response= requests.request("GET",url,headers=headers,params=params)
#     artist=response.json()
#     return artist["items"][1]["track"]["artists"][0]["id"]


# def get_random_genre(artist_seed):
#     token= get_token_for_spotify()
#     artist_id=artist_seed
#     params={"ids":artist_id}
#     headers={
#         "Authorization":"Bearer {}".format(token)
#     }
#     url=f"https://api.spotify.com/v1/artists"
#     response= requests.request("GET",url,headers=headers,params=params)
#     genre=response.json()
#     return genre["artists"][0]["genres"]

# def get_starting_point_playlist(focus_sentiment):
#     if focus_sentiment >= -1 and focus_sentiment<-0.7:
#         return "7mCzIltN0jFQ54GH02HMsY"
#     elif focus_sentiment>=-0.7 and focus_sentiment<-0.4:
#         return "37i9dQZF1DX0XUsuxWHRQd"
#     elif focus_sentiment>=-0.4 and focus_sentiment<0:
#         return "4y3WX0SZQ2cTLBovftfyiP"
#     elif focus_sentiment>=0 and focus_sentiment<.4:
#         return "37i9dQZF1DWV7EzJMK2FUI"
#     elif focus_sentiment>=.4 and focus_sentiment<0.7:
#         return "7vI0tN3yUn07dkK9T6p2pg"
#     elif focus_sentiment>=0.7 and focus_sentiment<=1:
#         return "37i9dQZF1DXaqCgtv7ZR3L"

# def get_recommended_music(playlist_id):
#     token= get_token()
#     track_seed=get_random_song(playlist_id)
#     artist_seed=get_random_artist(playlist_id)
#     genre_seed=get_random_genre(artist_seed)

#     limit=1
#     params={
#         "limit":limit,
#         "seed_artists":artist_seed,
#         "seed_genres":genre_seed,
#         "seed_tracks":track_seed,
#         "market":"US"
#         }
#     headers={
#         "Authorization":"Bearer {}".format(token)
#     }
#     url=f"https://api.spotify.com/v1/recommendations"
#     response= requests.request("GET",url,headers=headers,params=params)
#     recommended=response.json()
#     return recommended['tracks'][0]['name']



# def get_playlist(focus_sentiment):
#     playlist=[]
#     playlist_id=get_starting_point_playlist(focus_sentiment)
#     return get_recommended_music(playlist_id)



@app.route('/')
def home():
    return render_template("urmusic_form.html")

@app.route('/get_tweets', methods=["POST"])
def get_tweets():
    user_id=request.form["twitter-id"]
    tweets=get_tweets(user_id)

    # sentiments=[]

    # for tweet in tweets:
    #     sentiments.append("uno")
    #     sentiment=google_sentiment_analysis(tweet['text'])
    #     sentiments.append([sentiment.score, sentiment.magnitude])

    # focus_sentiment=get_focus_sentiment(sentiments)

    # music= get_playlist(focus_sentiment)
    # return music

    return tweets

def get_tweets(user_id):
    bearer_token=twitter_bearer_token
    header={"Authorization": "Bearer {}".format(bearer_token)}
    # params={"max_results":10}
    response=requests.request(
        "GET",
        "https://api.twitter.com/2/users/{}/tweets".format(user_id),
        headers=header,
        # params=params
    )
    tweets= response.json()["data"]
    # return tweets
    return json.dumps(tweets,indent=4,sort_keys=True)











