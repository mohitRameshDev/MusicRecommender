from dotenv import load_dotenv
import os
import base64
from requests import post
import json
import pickle
import streamlit as st

load_dotenv()
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

import atexit

# ...

class ImprovedSpotify(spotipy.Spotify):
    def __del__(self):
        try:
            if hasattr(self, '_session'):
                self._session.close()
        except Exception as e:
            pass

# Replace the original Spotify class with the improved one
spotipy.Spotify = ImprovedSpotify

auth_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(auth_manager=auth_manager)


def get_song_album_cover_url(song_name,artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        print(album_cover_url)
        return album_cover_url
    else:
        print("https://i.postimg.cc/0QNxYz4V/social.png")


music = pickle.load(open('df.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))



def recommender(song):
    index = music[music['song']==song].index[0]
    distances = sorted(list(enumerate(similarity[index])),reverse=True, key=lambda x: x[1])
    recommended_music_names= []
    recommended_music_posters = []
    for i in distances[1:6]:
        artist = music.iloc[i[0]].artist
        print(artist)
        print(music.iloc[i[0]].song)
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
        recommended_music_names.append(music.iloc[i[0]].song)
        
    return recommended_music_names,recommended_music_posters


st.header('Music Recommender System')

songlists = music['song'].values
selected_song = st.selectbox(
    "Type or select a song from the dropdown",
    songlists
)




if st.button('Show Recommendation'):
    try:
        recommended_music_names,recommended_music_posters = recommender(selected_song)
        col1, col2, col3, col4, col5= st.columns(5)
        with col1:
            st.text(recommended_music_names[0])
            st.image(recommended_music_posters[0])
        with col2:
            st.text(recommended_music_names[1])
            st.image(recommended_music_posters[1])

        with col3:
            st.text(recommended_music_names[2])
            st.image(recommended_music_posters[2])
        with col4:
            st.text(recommended_music_names[3])
            st.image(recommended_music_posters[3])
        with col5:
            st.text(recommended_music_names[4])
            st.image(recommended_music_posters[4])
    except:
        st.error("Sorry,Couldnt Fetch All Song Covers :(", icon="🚨")







