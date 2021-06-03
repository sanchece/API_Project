
import base64
import requests
import random


def get_rand():
    return random.randint(0,10)



# for spotify below
clientId = ''
clientSecret = ''


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

def get_random_song(playlist_id):
    token= get_token_for_spotify()
    params={"market":"US","limit":10}
    headers={
        "Authorization":"Bearer {}".format(token)
    }
    url=f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    response= requests.request("GET",url,headers=headers,params=params)
    song=response.json()
    rand=get_rand()
    return song["items"][rand]["track"]["id"]

def get_random_artist(playlist_id):
    token= get_token_for_spotify()

    params={"market":"US","limit":1}
    headers={
        "Authorization":"Bearer {}".format(token)
    }
    url=f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    response= requests.request("GET",url,headers=headers,params=params)
    artist=response.json()
    return artist["items"][0]["track"]["artists"][0]["id"]


def get_random_genre(artist_seed):
    token= get_token_for_spotify()
    artist_id=artist_seed
    params={"ids":artist_id}
    headers={
        "Authorization":"Bearer {}".format(token)
    }
    url=f"https://api.spotify.com/v1/artists"
    response= requests.request("GET",url,headers=headers,params=params)
    genre=response.json()
    return genre["artists"][0]["genres"]

def get_starting_point_playlist(focus_sentiment):
    if focus_sentiment >= -1 and focus_sentiment<-0.7:
        return "7mCzIltN0jFQ54GH02HMsY"
    elif focus_sentiment>=-0.7 and focus_sentiment<-0.4:
        return "37i9dQZF1DX0XUsuxWHRQd"
    elif focus_sentiment>=-0.4 and focus_sentiment<0:
        return "4y3WX0SZQ2cTLBovftfyiP"
    elif focus_sentiment>=0 and focus_sentiment<.4:
        return "37i9dQZF1DWV7EzJMK2FUI"
    elif focus_sentiment>=.4 and focus_sentiment<0.7:
        return "7vI0tN3yUn07dkK9T6p2pg"
    elif focus_sentiment>=0.7 and focus_sentiment<=1:
        return "37i9dQZF1DXaqCgtv7ZR3L"

def get_recommended_music(focus,playlist_id):
    token= get_token_for_spotify()
    track_seed=get_random_song(playlist_id)
    track_seed2=get_random_song(playlist_id)

    artist_seed=get_random_artist(playlist_id)
    genre_seed=get_random_genre(artist_seed)


    limit=10
    target_danceability=(focus+1)/2

    params={
        "limit":limit,
        "seed_artists":[artist_seed],
        "seed_genres":[genre_seed],
        "seed_tracks":[track_seed,track_seed2],
        "market":"US",
        "target_danceability":target_danceability
        }
    headers={
        "Authorization":"Bearer {}".format(token)
    }
    url=f"https://api.spotify.com/v1/recommendations"
    response= requests.request("GET",url,headers=headers,params=params)
    recommended=response.json()
    try:
        results=recommended['tracks'][0]
        return results
    except:
        return None



def get_playlist(focus_sentiment):
    playlist_id=get_starting_point_playlist(focus_sentiment)
    return get_recommended_music(focus_sentiment,playlist_id)

