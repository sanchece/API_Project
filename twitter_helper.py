import json
import requests
import os
# for twitter below
twitter_bearer_token=os.environ.get('TWITTER_TOKEN')




def get_tweets(user_id):
    bearer_token=twitter_bearer_token
    header={"Authorization": "Bearer {}".format(bearer_token)}
    params={"max_results":10}
    response=requests.request(
        "GET",
        "https://api.twitter.com/2/users/{}/tweets".format(user_id),
        headers=header,
        params=params
    )
    tweets= response.json()["data"]
    return tweets

def get_id(username):
    bearer_token=twitter_bearer_token
    header={"Authorization": "Bearer {}".format(bearer_token)}
    response=requests.request(
        "GET",
        "https://api.twitter.com/2/users/by/username/{}".format(username),
        headers=header
    )
    return response.json()["data"]["id"]