import base64
from models import Playlist
import requests
import random
import os

def get_rand():
    return random.randint(0,10)

# for spotify below
clientId = os.environ.get('SPOTIFY_ID')
clientSecret = os.environ.get('SPOTIFY_SECRET')


def get_urmusic(focus_sentiment):
    track_seeds=[]
    artist_seeds=[]

    playlists=determine_starting_playlists(focus_sentiment)
    for playlist in playlists:
        list_of_tracks=get_tracks(playlist)
        artist_seeds.append(get_artist_seed(list_of_tracks))
        track_seeds.append(get_track_seed(list_of_tracks))


    featured_playlists=get_featured_playlists()
    for playlist in featured_playlists:
        list_of_tracks=get_tracks(playlist)
        artist_seeds.append(get_artist_seed(list_of_tracks))
        track_seeds.append(get_track_seed(list_of_tracks))

    ur_music=get_request_urmusic(track_seeds,artist_seeds,focus_sentiment)
    return ur_music

    
def get_request_urmusic(track_seeds,artist_seeds,focus_sentiment):
    ur_music=[]
    token= get_token_for_spotify()
    target_danceability=get_danceability(focus_sentiment)
    for track in range(len(track_seeds)):
        limit=4
        params={
            "limit":limit,
            "seed_artists":artist_seeds[track],
            "seed_tracks":track_seeds[track],
            "market":"US",
            "target_danceability":target_danceability
            }
        headers={
            "Authorization":"Bearer {}".format(token)
        }
        url=f"https://api.spotify.com/v1/recommendations"
        response= requests.request("GET",url,headers=headers,params=params)
        recommended=response.json()["tracks"]
        for track in recommended:
            ur_music.append(track)
    
    return ur_music

def get_token_for_spotify():
    url="https://accounts.spotify.com/api/token"
    auth_str ='{}:{}'.format(clientId, clientSecret)
    headers={
        "Content-Type":"application/x-www-form-urlencoded",
        "Authorization":"Basic "+base64.urlsafe_b64encode(auth_str.encode()).decode(),
        }
    data={
        'grant_type': 'client_credentials'
        }
    result=requests.post(url,data=data, headers=headers)
    token=result.json()
    return token['access_token']
def get_danceability(focus_sentiment):
    return (focus_sentiment+1)/2

def get_playlist_from_sentiment(focus_sentiment):
    if focus_sentiment==-1:
        # Hardcore Punk Rock
        return "7mCzIltN0jFQ54GH02HMsY"
    elif focus_sentiment >-1 and focus_sentiment<=-0.9:
        #Metal/ Hard Rock
        return "1GXRoQWlxTNQiMNkOe7RqA"
    elif focus_sentiment >-0.9 and focus_sentiment<=-0.8:
        # Dream Pop
        return "37i9dQZF1DX6uhsAfngvaD"
    elif focus_sentiment >-0.8 and focus_sentiment<=-0.7:
        # Indie Rock
        return "7lnCgcTxLTTcOqvgoS80sC"
    elif focus_sentiment >-0.7 and focus_sentiment<=-0.6:
        # EDM
        return "2e3dcRuo9uDH6qD3NOGKAL"
    elif focus_sentiment >-0.6 and focus_sentiment<=-0.5:
        # Alternative Rock
        return "37i9dQZF1DX9GRpeH4CL0S"
    elif focus_sentiment >-0.5 and focus_sentiment<=-0.4:
        # R&B
        return "37i9dQZF1DX4SBhb3fqCJd"
    elif focus_sentiment >-0.4 and focus_sentiment<=-0.3:
        # Blues
        return "37i9dQZF1DXd9rSDyQguIk"
    elif focus_sentiment >-0.3 and focus_sentiment<=-0.2:
        # Indie Folk
        return "5tOffZXVBFTMS7mkKQ3tpX"
    elif focus_sentiment >-0.2 and focus_sentiment<=-0.1:
        # country
        return "37i9dQZF1DX13ZzXoot6Jc"
    elif focus_sentiment >-0.1 and focus_sentiment<=0:
        # Classical
        return "37i9dQZF1DWWEJlAGA9gs0"
    elif focus_sentiment >0 and focus_sentiment<0.1:
        # trance
        return "37i9dQZF1DXbtYAdenGE9U"
    elif focus_sentiment >=0.1 and focus_sentiment<0.2:
        #mellow
        return "37i9dQZF1DWTQwRw56TKNc"
    elif focus_sentiment >=0.2 and focus_sentiment<0.3:
        # Jazz
        return "37i9dQZF1DXbITWG1ZJKYt"
    elif focus_sentiment >=0.3 and focus_sentiment<0.4:
        # Reggae
        return "37i9dQZF1DXbSbnqxMTGx9"
    elif focus_sentiment >=0.4 and focus_sentiment<0.5:
        # Rap
        return "37i9dQZF1DX0XUsuxWHRQd"
    elif focus_sentiment >=0.5 and focus_sentiment<0.6:
        # Love
        return "5KbTzqKBqxQRD8OBtJTZrS"
    elif focus_sentiment >=0.6 and focus_sentiment<0.7:
        # Latino
        return "37i9dQZF1DX10zKzsJ2jva"
    elif focus_sentiment >=0.7 and focus_sentiment<0.8:
        # Pop
        return "37i9dQZF1DX2L0iB23Enbq"
    elif focus_sentiment >=0.8 and focus_sentiment<0.9:
        # Disco
        return "37i9dQZF1DX2GKumqRIZ7g"
    elif focus_sentiment >=0.9 and focus_sentiment<1:
        # Funk
        return "37i9dQZF1DWWvhKV4FBciw"
    elif focus_sentiment ==1:
        # Salsa
        return "37i9dQZF1DX7SeoIaFyTmA"

def determine_starting_playlists(focus_sentiment):
    playlists=[]
    # get playlists based on sentiment
    focus_sentiments=[focus_sentiment,focus_sentiment-0.1,focus_sentiment+0.1]
    for sentiment in focus_sentiments:
        playlists.append(get_playlist_from_sentiment(sentiment))
    return playlists
def get_tracks(playlist_id):
    token= get_token_for_spotify()
    params={"market":"US","limit":10}
    headers={
        "Authorization":"Bearer {}".format(token)
    }
    url=f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    response= requests.request("GET",url,headers=headers,params=params)
    tracks=response.json()
    return tracks
def get_track_seed(tracks):
    rand=random.randint(0,len(tracks["items"])-1)
    track_seed=tracks["items"][rand]["track"]["id"]
    return track_seed
def get_artist_seed(tracks):
    rand=random.randint(0,len(tracks["items"])-1)
    artist_seed=tracks["items"][rand]["track"]["artists"][0]["id"]
    return artist_seed

def get_featured_playlists():
    token= get_token_for_spotify()
    params={"market":"US","limit":3}
    headers={
        "Authorization":"Bearer {}".format(token)
    }
    url=f"https://api.spotify.com/v1/browse/featured-playlists"
    response= requests.request("GET",url,headers=headers,params=params)
    ids=response.json()["playlists"]["items"]
    featured_playlists=[]
    for playlist in ids:
        featured_playlists.append(playlist["id"])
    return featured_playlists

