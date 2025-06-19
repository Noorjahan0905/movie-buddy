import requests
import random
import streamlit as st

def fetch_poster(movie_title):
    """
    Fetch movie poster from TMDb API
    
    Parameters:
    movie_title (str): Title of the movie to fetch poster for
    
    Returns:
    str: URL of the movie poster or a placeholder if not found
    """
    # Get API key from session state
    API_KEY = st.session_state.get('TMDB_API_KEY')
    
    # If no API key, return placeholder
    if not API_KEY or API_KEY == "your_tmdb_api_key_here":
        color = "%06x" % random.randint(0, 0xFFFFFF)
        return f"https://via.placeholder.com/300x450/{color}/FFFFFF?text={movie_title.replace(' ', '+')}"
    
    try:
        # Make API request
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_title}"
        response = requests.get(url)
        data = response.json()
        
        # Check if the API key is valid
        if 'success' in data and data['success'] == False:
            # Generate random color for the placeholder
            color = "%06x" % random.randint(0, 0xFFFFFF)
            return f"https://via.placeholder.com/300x450/{color}/FFFFFF?text={movie_title.replace(' ', '+')}"
        
        # Check if we have results
        if 'results' in data and data['results']:
            poster_path = data['results'][0].get('poster_path', '')
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
        
        # No poster found, create a nice placeholder
        color = "%06x" % random.randint(0, 0xFFFFFF)
        return f"https://via.placeholder.com/300x450/{color}/FFFFFF?text={movie_title.replace(' ', '+')}"
        
    except Exception as e:
        # In case of any error, return a placeholder
        color = "%06x" % random.randint(0, 0xFFFFFF)
        return f"https://via.placeholder.com/300x450/{color}/FFFFFF?text={movie_title.replace(' ', '+')}"

def fetch_movie_details(movie_id):
    """
    Fetch detailed movie information from TMDb API
    
    Parameters:
    movie_id (int): TMDb ID of the movie
    
    Returns:
    dict: Movie details or None if not found
    """
    # Get API key from session state
    API_KEY = st.session_state.get('TMDB_API_KEY')
    
    # If no API key, return None
    if not API_KEY or API_KEY == "your_tmdb_api_key_here":
        return None
    
    try:
        # Make API request
        url = f"https://api.themoviedb.org/3/movie/{movie_id}"
        params = {
            "api_key": API_KEY,
            "language": "en-US"
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def search_movie(query):
    """
    Search for movies by title
    
    Parameters:
    query (str): Movie title to search for
    
    Returns:
    list: List of matching movies or empty list if none found
    """
    # Get API key from session state
    API_KEY = st.session_state.get('TMDB_API_KEY')
    
    # If no API key, return empty list
    if not API_KEY or API_KEY == "your_tmdb_api_key_here":
        return []
    
    try:
        # Make API request
        url = "https://api.themoviedb.org/3/search/movie"
        params = {
            "api_key": API_KEY,
            "language": "en-US",
            "query": query,
            "page": 1,
            "include_adult": False
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            return data.get("results", [])
        return []
    except:
        return []