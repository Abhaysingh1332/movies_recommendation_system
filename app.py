
import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_title):
    try:
        # Clean up the movie title for the API request
        title = movie_title.replace(" ", "+")
        
        # Make request to OMDB API
        omdb_api_key = "e522615a"  # Your OMDB API key
        response = requests.get(
            f"http://www.omdbapi.com/?t={title}&apikey={omdb_api_key}",
            timeout=10
        )
        
        data = response.json()
        
        # Check if response is successful and contains a poster
        if data.get('Response') == 'True' and data.get('Poster') != 'N/A':
            return data.get('Poster')
        else:
            print(f"No poster found for {movie_title}")
            return "https://via.placeholder.com/500x750?text=No+Image"
            
    except Exception as e:
        print(f"Error fetching poster for {movie_title}: {e}")
        return "https://via.placeholder.com/500x750?text=No+Image"



# Function to recommend movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        # Get movie title instead of ID
        movie_title = movies.iloc[i[0]].title
        recommended_movies.append(movie_title)
        
        # Fetch poster using title
        recommended_movies_posters.append(fetch_poster(movie_title))

    return recommended_movies, recommended_movies_posters


# Load the movie data and similarity matrix
movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit UI
st.title('Movie Recommender System')

# Dropdown menu to select a movie
selected_movie_name = st.selectbox(
    'Select a movie to get recommendations:',
    movies['title'].values
)

# Recommend button
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])






