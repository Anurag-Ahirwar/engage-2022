import streamlit as st
import pickle
import pandas as pd
import numpy as np
# import tqdm
import requests
import time
st.set_page_config(layout="wide")
st.title('Recommender System')
# movie part -----------------------------------------------
@st.cache
def fetch_poster(movie_id):
     response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=f8e70ae3406ec61d2127b34a92c7ce32&language=en-US'.format(movie_id))
     data = response.json()
     return "https://image.tmdb.org/t/p/w500/"+data['poster_path']

def recommend(movie):
     movie_index = movies[movies['title'] == movie].index[0]
     distances = similarities[movie_index]
     movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

     recommended_movies=[]
     recommended_movies_poster=[]
     for i in movies_list:
          movie_id = movies.iloc[i[0]].movie_id
          recommended_movies.append(movies.iloc[i[0]].title)
          recommended_movies_poster.append(fetch_poster(movie_id))
     return recommended_movies,recommended_movies_poster


movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarities = pickle.load(open('similarities.pkl','rb'))

# song part--------------------------------------------------------
@st.cache
class Spotify_Recommendation():
    def __init__(self, dataset):
        self.dataset = dataset
    def recommend(self, songs, amount =1):
        distance =[]
        song = self.dataset[(self.dataset.name.str.lower()==songs.lower())].head(1).values[0]
        rec = self.dataset[self.dataset.name.str.lower() != songs.lower()]
        for songs in rec.values:
            d = 0
            for col in np.arange(len(rec.columns)):
                if not col in [1,6,12,14,18,19]:
                    d = d + np.absolute(float(song[col])-float(songs[col]))
            distance.append(d)
        rec['distance'] = distance
        rec = rec.sort_values('distance')
        columns = ['artists','songs_name']
        return rec[columns][:amount]

song_dict = pickle.load(open('songs_dict.pkl','rb'))
spotify = pd.DataFrame(song_dict)
# display part ----------------------------------------------------------
# movie-------------------------------
recommendation_of_what = st.selectbox('Recommendation for : MOVIES OR SONGS',('MOVIES','SONGS'))

if recommendation_of_what == 'MOVIES':
     selected_movie_name = st.selectbox(
          'Recommendation based on',
          (movies['title'].values))
     if st.button('Recommend'):

          name, poster = recommend((selected_movie_name))

          progress = st.progress(0)
          for i in range(100):
               time.sleep(0.1)
               progress.progress(i + 1)
          st.text('Recommended Movies based on your choice')
          col1, col2, col3, col4, col5 = st.columns(5)

          with col1:
               st.write(name[0])
               st.image(poster[0])
          with col2:
               st.write(name[1])
               st.image(poster[1])
          with col3:
               st.write(name[2])
               st.image(poster[2])
          with col4:
               st.write(name[3])
               st.image(poster[3])
          with col5:
               st.write(name[4])
               st.image(poster[4])
# songs------------------------------------------
if recommendation_of_what == 'SONGS':
     selected_song_name = st.selectbox(
          'Recommendation based on',
          (spotify['name'].values))
     if st.button('Recommend'):
          recommendation = Spotify_Recommendation(spotify)

          display_songs = recommendation.recommend(selected_song_name,10)
          progress = st.progress(0)
          for i in range(100):
               time.sleep(0.1)
               progress.progress(i+1)

          st.text('Recommended Songs based on your choice')
          st.dataframe(display_songs,width = 1200,height= 1200)


