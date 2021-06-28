# UrMusic 
### URL
> [Visit UrMusic](http://ur-music.herokuapp.com/) 
### Overview 
>UrMusic is an online web application that will help you find music using the overall mood of your latest tweets! 
By signing up you will be able to save playlist in UrMusic profile.
##### More about how the app works ...
>This web application works by fetching the latest public tweets found in your Twitter timeline using Twitter's API and running a sentiment analysis on the list of extracted tweets.  
An overall (mood) sentiment is determined using the help of Google's Cloud Sentiment Analysis API, and then the right tracks to match your overall sentiment are found using various Spotify API endpoints.

### Features
>* UrMusic sends requests to 3 different APIs including Google Cloud Sentiment Analysis, Twitter API, Spotify API
>* Data is stored and can be manipulated in a postgreSQL database which can be set up on your local machine or online
>* Passwords are bcrypted to store user's passwords 
>* A Flask session is created to keep user logged in while navigating the website
>* A media player is displayed and available to play all the queued tracks instantly 
>* Tailored front-end for a variety of screen sizes from smart phones to PC monitors

### Technology Stack
>* Twitter API
>   * Twitter developer account required [link](https://developer.twitter.com/en/docs/getting-started)
>   * Credentials can be declared on top of twitter_helper.py
>* Google Cloud Natural Language API
>   * Google developer account required [link](https://cloud.google.com/natural-language/docs/analyzing-sentiment)
>   * Credentials must be set up using Google's [Athentication Overview](https://cloud.google.com/docs/authentication)
>* Spotify
>   * Spotify developer account required [link](https://developer.twitter.com/en/docs/getting-started)
>   * Credentials can be declared on top of spotify_helper.py
>* Flask
>* SQLAlchemy
>* PostgreSQL
>* WTForms

### Set Up
> * Set up a virtual enviroment to pip install flask
> * pip install all dependencies using the requirements.txt file
> * Set up postgresql database and map it in app.py line 17 or line 18


### User Flow

>1. User is welcomed and an overview is displayed on the homepage. The navbar has 2 buttons giving a user the option to Login to an existing account or Sign-Up for the first time.
>![image](https://user-images.githubusercontent.com/78108711/123565004-71858800-d789-11eb-894b-1aeee7a8a982.png)
>2. Forms are displayed to Login or Sign-Up when clicking on the navbar options
> An error is displayed on the form if the password does not meet the requirements, the Twitter handle does not exist or an email is not provided.
>![image](https://user-images.githubusercontent.com/78108711/123565494-16549500-d78b-11eb-9fa4-354fefe30ee9.png)
>![image](https://user-images.githubusercontent.com/78108711/123565506-1e143980-d78b-11eb-8f49-89319daa17e7.png)
>3. After signing up a playlist of 24 tracks are automatically displayed using the overall sentiment determined using the Twitter handle provided on the Sign-Up form.   
>  A form is displayed to name and save the playlist to UrMusic profile.  
>Once signed in, the navbar buttons change to Logout or go to Profile.
>![image](https://user-images.githubusercontent.com/78108711/123566218-27060a80-d78d-11eb-9452-e05f97b640b9.png)
>4. In Profile, a signed in user can find their saved playlists.  
>Hovering on the playlist will display an Orange background on the playlist and clicking on it will display the tracks in that playlist.  
>Get New Playlist button will run a new sentiment analysis on your latest tweets and display a brand new playlist.
>![image](https://user-images.githubusercontent.com/78108711/123568093-9aaa1680-d791-11eb-916e-becafb27fd7b.png)
>5. Logout to clear your session.



