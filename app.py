import streamlit as st
import requests
from recommender import get_recommendations
import base64
import random
import time

# --- Page configuration ---
st.set_page_config(
    page_title="Movie Buddy",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Session state initialization (put this at the top, after imports) ---
if "search_movie" not in st.session_state:
    st.session_state["search_movie"] = ""
if "trigger_search" not in st.session_state:
    st.session_state["trigger_search"] = False

# --- Enhanced CSS with animations and better interactivity ---
def add_bg_and_styling():
    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
    <style>
        html, body, .stApp {
            font-family: 'Poppins', sans-serif !important;
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%) !important;
            color: #f8f9fa;
            overflow-x: hidden;
        }
        
        /* Animated background particles */
        .background-animation {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
            opacity: 0.1;
        }
        
        /* Main title with enhanced animation */
        .main-title {
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
            background-size: 400% 400%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-align: center;
            margin: 1.2rem 0 0.7rem 0;
            animation: gradientShift 3s ease-in-out infinite;
            text-shadow: 0 0 18px rgba(255, 107, 107, 0.2);
            letter-spacing: 1.2px;
        }
        
        @keyframes gradientShift {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        
        /* Floating animation for subtitle */
        .subtitle {
            color: #b8c6db;
            font-size: 1.1rem;
            text-align: center;
            margin-bottom: 1.2rem;
            animation: float 3s ease-in-out infinite;
            font-weight: 300;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
        }
        
        /* Search container with glassmorphism */
        .search-container {
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(14px);
            border: 1px solid rgba(255, 255, 255, 0.13);
            border-radius: 16px;
            padding: 1.2rem 1rem 1.2rem 1rem;
            margin: 1.2rem auto 0.7rem auto;
            max-width: 700px;
            box-shadow: 0 4px 18px rgba(0, 0, 0, 0.13);
            position: relative;
            overflow: hidden;
        }
        
        .search-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.07), transparent);
            animation: shimmer 3s infinite;
        }
        
        @keyframes shimmer {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        
        /* Enhanced input styling */
        .stTextInput > div > div > input {
            background: rgba(255, 255, 255, 0.04) !important;
            border: 2px solid rgba(255, 107, 107, 0.5) !important;
            color: #fff !important;
            border-radius: 30px !important;
            padding: 0.7rem 2rem 0.7rem 2rem !important;
            font-size: 1.05rem !important;
            transition: all 0.2s ease !important;
            backdrop-filter: blur(7px) !important;
        }
        
        .stTextInput > div > div > input:focus {
            border: 2px solid #ff6b6b !important;
            box-shadow: 0 0 10px rgba(255, 107, 107, 0.2) !important;
            background: rgba(255, 255, 255, 0.07) !important;
        }
        
        .search-icon {
            position: absolute;
            left: 2rem;
            top: 50%;
            transform: translateY(-50%);
            color: #ff6b6b;
            font-size: 1.5rem;
            z-index: 10;
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 0.7; }
            50% { opacity: 1; }
        }
        
        /* Button with hover effects */
        .stButton > button {
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4) !important;
            color: white !important;
            font-weight: 600 !important;
            border: none !important;
            padding: 0.7rem 1.5rem !important;
            border-radius: 30px !important;
            font-size: 1.05rem !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 4px 12px rgba(255, 107, 107, 0.18) !important;
            position: relative !important;
            overflow: hidden !important;
            text-transform: uppercase !important;
            letter-spacing: 0.7px !important;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px) scale(1.03) !important;
            box-shadow: 0 8px 18px rgba(255, 107, 107, 0.25) !important;
        }
        
        .stButton > button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            transition: left 0.5s;
        }
        
        .stButton > button:hover::before {
            left: 100%;
        }
        
        /* Sidebar styling */
        .sidebar-content {
            background: rgba(255, 255, 255, 0.04);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: 10px;
            padding: 1rem;
            margin: 0.7rem 0;
            transition: all 0.2s ease;
        }
        
        .sidebar-content:hover {
            background: rgba(255, 255, 255, 0.09);
            transform: translateY(-1px);
        }
        
        /* Enhanced sample movie buttons */
        .stButton > button {
            background: linear-gradient(135deg, rgba(255, 107, 107, 0.15), rgba(78, 205, 196, 0.15)) !important;
            color: #e2e8f0 !important;
            font-weight: 500 !important;
            border: 1px solid rgba(255, 107, 107, 0.3) !important;
            border-radius: 12px !important;
            padding: 0.8rem 1rem !important;
            transition: all 0.3s ease !important;
            font-size: 0.9rem !important;
            backdrop-filter: blur(10px) !important;
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, rgba(255, 107, 107, 0.25), rgba(78, 205, 196, 0.25)) !important;
            border-color: rgba(255, 107, 107, 0.6) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(255, 107, 107, 0.2) !important;
        }
        
        /* Main search button styling */
        .stButton[data-testid="find_similar_btn"] > button {
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4) !important;
            color: white !important;
            font-weight: 600 !important;
            border: none !important;
            padding: 1.2rem 2.5rem !important;
            border-radius: 50px !important;
            font-size: 1.2rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 10px 30px rgba(255, 107, 107, 0.3) !important;
            text-transform: uppercase !important;
            letter-spacing: 1px !important;
        }
        
        .stButton[data-testid="find_similar_btn"] > button:hover {
            transform: translateY(-3px) scale(1.05) !important;
            box-shadow: 0 15px 40px rgba(255, 107, 107, 0.5) !important;
        }
        
        /* Movie cards with enhanced styling */
        .movie-card {
            background: rgba(255, 255, 255, 0.04);
            backdrop-filter: blur(8px);
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: 12px;
            padding: 1rem 1.2rem;
            margin: 0.7rem 0;
            transition: all 0.2s ease;
            position: relative;
            overflow: hidden;
        }
        
        .movie-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #ff6b6b, #4ecdc4, #45b7d1);
            transform: translateX(-100%);
            transition: transform 0.5s ease;
        }
        
        .movie-card:hover {
            transform: translateY(-3px) scale(1.01);
            box-shadow: 0 8px 18px rgba(0, 0, 0, 0.13);
            background: rgba(255, 255, 255, 0.08);
        }
        
        .movie-card:hover::before {
            transform: translateX(0);
        }
        
        .movie-title {
            color: #ff6b6b;
            font-size: 1.1rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }
        
        .movie-overview {
            color: #e2e8f0;
            font-size: 0.97rem;
            line-height: 1.5;
            opacity: 0.92;
            margin-bottom: 0.2rem;
        }
        
        /* Loading animation */
        .loading-container {
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 1.2rem;
        }
        
        .loading-spinner {
            width: 50px;
            height: 50px;
            border: 3px solid rgba(255, 107, 107, 0.3);
            border-top: 3px solid #ff6b6b;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        /* Success message styling */
        .success-message {
            background: rgba(76, 175, 80, 0.13);
            border: 1px solid rgba(76, 175, 80, 0.22);
            border-radius: 8px;
            padding: 0.7rem 1rem;
            margin: 0.7rem 0;
            text-align: center;
            font-weight: 500;
        }
        
        /* Footer enhancement */
        .footer {
            text-align: center;
            color: #94a3b8;
            font-size: 0.95rem;
            margin-top: 1.2rem;
            padding: 1.2rem 0 0.5rem 0;
            background: rgba(255, 255, 255, 0.01);
            border-top: 1px solid rgba(255, 255, 255, 0.07);
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .main-title {
                font-size: 1.7rem;
            }
            .search-container {
                padding: 0.7rem 0.5rem;
                margin: 0.7rem;
            }
            .stTextInput > div > div > input {
                padding: 0.5rem 1.2rem 0.5rem 1.2rem !important;
                font-size: 0.95rem !important;
            }
        }
        
        /* Hide Streamlit branding */
        .stApp > header {
            background-color: transparent;
        }
        
        .stApp > div > div > div > div > div > section > div {
            padding-top: 1rem;
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.1);
        }
        
        ::-webkit-scrollbar-thumb {
            background: rgba(255, 107, 107, 0.5);
            border-radius: 4px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 107, 107, 0.7);
        }
    </style>
    """, unsafe_allow_html=True)

add_bg_and_styling()

# --- Animated background particles ---
st.markdown("""
<div class="background-animation">
    <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
        <defs>
            <pattern id="star" viewBox="0 0 20 20" width="20" height="20" patternUnits="userSpaceOnUse">
                <circle cx="10" cy="10" r="1" fill="#ff6b6b" opacity="0.3">
                    <animate attributeName="opacity" values="0.3;1;0.3" dur="3s" repeatCount="indefinite"/>
                </circle>
            </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#star)"/>
    </svg>
</div>
""", unsafe_allow_html=True)

# --- Utility: Generate a placeholder poster image ---
def placeholder_poster(movie_title):
    color = "%06x" % random.randint(0, 0xFFFFFF)
    return f"https://via.placeholder.com/300x450/{color}/FFFFFF?text={movie_title.replace(' ', '+')}"

# --- API key handling ---
if 'TMDB_API_KEY' not in st.session_state:
    try:
        st.session_state.TMDB_API_KEY = st.secrets["TMDB_API_KEY"]
    except Exception:
        st.session_state.TMDB_API_KEY = None

# --- Fetch movie poster with error handling ---
def fetch_poster(movie_title):
    """Fetch poster from TMDb or return a placeholder."""
    API_KEY = st.session_state.get('TMDB_API_KEY')
    if not API_KEY or API_KEY == "your_tmdb_api_key_here":
        return placeholder_poster(movie_title)
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_title}"
        response = requests.get(url, timeout=5)
        data = response.json()
        if 'success' in data and data['success'] is False:
            return placeholder_poster(movie_title)
        if 'results' in data and data['results']:
            poster_path = data['results'][0].get('poster_path', '')
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
        return placeholder_poster(movie_title)
    except Exception:
        return placeholder_poster(movie_title)

# --- Show API warning if needed ---
if not st.session_state.TMDB_API_KEY or st.session_state.TMDB_API_KEY == "your_tmdb_api_key_here":
    st.info("💡 **Pro Tip:** Set up your TMDb API key for movie posters! [Go to API Setup](./3_API_Setup)")

# --- Sidebar content ---
with st.sidebar:
    # Enhanced sidebar header
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem; padding: 1rem;">
        <div style="
            background: linear-gradient(135deg, #ff6b6b, #4ecdc4);
            width: 80px;
            height: 80px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 1rem auto;
            animation: float 3s ease-in-out infinite;
            box-shadow: 0 10px 30px rgba(255, 107, 107, 0.3);
        ">
            <i class="fa-solid fa-film" style="font-size: 2.5rem; color: white;"></i>
        </div>
        <h2 style="color: #ff6b6b; margin: 0; font-weight: 700;">Movie Buddy</h2>
        <p style="color: #b8c6db; margin: 0.5rem 0 0 0; font-size: 0.9rem;">AI-Powered Cinema Discovery</p>
    </div>
    """, unsafe_allow_html=True)
    
    # About section with enhanced cards
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.1), rgba(78, 205, 196, 0.1));
        border: 1px solid rgba(255, 107, 107, 0.2);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
    ">
        <h3 style="color: #ff6b6b; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
            <i class="fa-solid fa-brain"></i> How It Works
        </h3>
        <div style="space-y: 1rem;">
            <div style="display: flex; align-items: center; gap: 0.8rem; margin-bottom: 0.8rem; padding: 0.5rem; background: rgba(255, 255, 255, 0.05); border-radius: 8px;">
                <i class="fa-solid fa-search" style="color: #4ecdc4; font-size: 1.2rem;"></i>
                <span style="color: #e2e8f0; font-size: 0.9rem;"><strong>Text Analysis:</strong> TF-IDF vectorization</span>
            </div>
            <div style="display: flex; align-items: center; gap: 0.8rem; margin-bottom: 0.8rem; padding: 0.5rem; background: rgba(255, 255, 255, 0.05); border-radius: 8px;">
                <i class="fa-solid fa-calculator" style="color: #45b7d1; font-size: 1.2rem;"></i>
                <span style="color: #e2e8f0; font-size: 0.9rem;"><strong>Similarity:</strong> Cosine matching</span>
            </div>
            <div style="display: flex; align-items: center; gap: 0.8rem; margin-bottom: 0.8rem; padding: 0.5rem; background: rgba(255, 255, 255, 0.05); border-radius: 8px;">
                <i class="fa-solid fa-ranking-star" style="color: #96ceb4; font-size: 1.2rem;"></i>
                <span style="color: #e2e8f0; font-size: 0.9rem;"><strong>Ranking:</strong> Smart recommendations</span>
            </div>
        </div>
        <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(255, 255, 255, 0.1);">
            <span style="color: #94a3b8; font-size: 0.8rem;">
                <i class="fa-solid fa-database" style="margin-right: 0.5rem;"></i>
                Data: TMDb 5000 Movie Dataset
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick stats section
    st.markdown("""
    <div style="
        background: linear-gradient(45deg, rgba(69, 183, 209, 0.15), rgba(150, 206, 180, 0.15));
        border: 1px solid rgba(69, 183, 209, 0.3);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        text-align: center;
    ">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
            <div>
                <div style="font-size: 1.8rem; font-weight: bold; color: #4ecdc4;">5000+</div>
                <div style="font-size: 0.8rem; color: #b8c6db;">Movies</div>
            </div>
            <div>
                <div style="font-size: 1.8rem; font-weight: bold; color: #45b7d1;">AI</div>
                <div style="font-size: 0.8rem; color: #b8c6db;">Powered</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sample movies section with enhanced grid
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, rgba(150, 206, 180, 0.1), rgba(255, 107, 107, 0.1));
        border: 1px solid rgba(150, 206, 180, 0.2);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
    ">
        <h3 style="color: #96ceb4; margin-bottom: 1.2rem; display: flex; align-items: center; gap: 0.5rem;">
            <i class="fa-solid fa-fire"></i> Popular Picks
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Create a 2x4 grid for sample movies
    sample_movies = [
        ("Inception", "fa-brain", "#ff6b6b"),
        ("The Dark Knight", "fa-mask", "#4ecdc4"),
        ("Interstellar", "fa-rocket", "#45b7d1"),
        ("The Matrix", "fa-desktop", "#96ceb4"),
        ("Pulp Fiction", "fa-gun", "#ffa726"),
        ("Avatar", "fa-tree", "#66bb6a"),
        ("Titanic", "fa-ship", "#42a5f5"),
        ("The Godfather", "fa-crown", "#ab47bc")
    ]
    
    # Display movies in a clean grid
    for i in range(0, len(sample_movies), 2):
        col1, col2 = st.columns(2)
        
        # First movie in pair
        with col1:
            movie, icon, color = sample_movies[i]
            if st.button(
                movie, 
                key=f"sample_{movie}",
                help=f"Get recommendations for '{movie}'",
                use_container_width=True
            ):
                st.session_state.search_movie = movie
                st.session_state.trigger_search = True
                st.rerun()
        
        # Second movie in pair (if exists)
        if i + 1 < len(sample_movies):
            with col2:
                movie, icon, color = sample_movies[i + 1]
                if st.button(
                    movie, 
                    key=f"sample_{movie}",
                    help=f"Get recommendations for '{movie}'",
                    use_container_width=True
                ):
                    st.session_state.search_movie = movie
                    st.session_state.trigger_search = True
                    st.rerun()

# --- Main content ---
st.markdown("<h1 class='main-title'><i class='fa-solid fa-film'></i> Movie Buddy</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'><i class='fa-solid fa-sparkles'></i> Discover your next favorite film with AI-powered recommendations</p>", unsafe_allow_html=True)

# --- Enhanced search section ---
st.markdown("""
<style>
.animated-gradient-box {
    border-radius: 24px;
    background: rgba(30, 34, 54, 0.7);
    box-shadow: 0 6px 32px 0 rgba(0,0,0,0.18);
    border: 3px solid;
    border-image: linear-gradient(90deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #ff6b6b) 1;
    animation: borderMove 4s linear infinite;
    padding: 1.7rem 1.2rem 1.7rem 1.2rem;
    margin: 1.5rem auto 0.5rem auto;
    max-width: 700px;
    position: relative;
    overflow: hidden;
    transition: box-shadow 0.3s;
    display: flex;
    flex-direction: column;
    align-items: center;
}
@keyframes borderMove {
    0% { border-image-source: linear-gradient(90deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #ff6b6b); }
    100% { border-image-source: linear-gradient(270deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #ff6b6b); }
}
.pulse-icon {
    display: inline-block;
    animation: pulseIcon 1.5s infinite;
}
@keyframes pulseIcon {
    0%, 100% { transform: scale(1); filter: drop-shadow(0 0 0 #ff6b6b); }
    50% { transform: scale(1.18); filter: drop-shadow(0 0 8px #ff6b6b); }
}
.gradient-title {
    font-size: 1.7rem;
    font-weight: 900;
    background: linear-gradient(90deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
    background-size: 200% 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-shadow: 0 2px 12px rgba(255,107,107,0.10);
    animation: gradientShift 3s ease-in-out infinite;
    display: inline-block;
    margin-left: 0.5rem;
    position: relative;
}
.gradient-title::after {
    content: '';
    display: block;
    height: 4px;
    width: 80%;
    margin: 0.3rem auto 0 auto;
    border-radius: 2px;
    background: linear-gradient(90deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4);
    animation: underlineAnim 2.5s linear infinite;
}
@keyframes underlineAnim {
    0% { width: 0; opacity: 0.2; }
    30% { width: 80%; opacity: 1; }
    100% { width: 0; opacity: 0.2; }
}
@keyframes gradientShift {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}
.fadein-subtitle {
    color: #b8c6db;
    font-size: 1.01rem;
    margin-top: 0.5rem;
    opacity: 0;
    animation: fadeInSubtitle 1.2s 0.5s forwards;
    font-weight: 400;
}
@keyframes fadeInSubtitle {
    to { opacity: 1; }
}
/* Glassmorphism for results */
.results-glass {
    background: rgba(255,255,255,0.08);
    border-radius: 18px;
    box-shadow: 0 4px 24px rgba(0,0,0,0.13);
    padding: 1.2rem 1.2rem 0.7rem 1.2rem;
    margin: 1.2rem auto 0.7rem auto;
    max-width: 900px;
    backdrop-filter: blur(10px);
    border: 1.5px solid rgba(255,255,255,0.13);
    position: relative;
}
/* Recommendation card animation */
@keyframes fadeInCard {
    from { opacity: 0; transform: translateY(30px) scale(0.97); }
    to { opacity: 1; transform: translateY(0) scale(1); }
}
.movie-card {
    animation: fadeInCard 0.7s cubic-bezier(.39,.575,.56,1) both;
    transition: box-shadow 0.2s, background 0.2s, transform 0.2s;
}
.movie-card:hover {
    box-shadow: 0 8px 32px rgba(255,107,107,0.13), 0 2px 8px rgba(78,205,196,0.10);
    background: rgba(255,255,255,0.13);
    transform: translateY(-3px) scale(1.01);
}
.stButton > button, .stButton > button:focus {
    outline: none !important;
    box-shadow: 0 2px 10px rgba(255,107,107,0.10) !important;
}
.stButton > button:hover {
    background: linear-gradient(90deg, #ff6b6b, #4ecdc4) !important;
    color: #fff !important;
    transform: scale(1.04) !important;
}
/* Footer gradient border */
.footer {
    border-top: 3px solid;
    border-image: linear-gradient(90deg, #ff6b6b, #4ecdc4, #45b7d1, #96ceb4, #ff6b6b) 1;
    margin-top: 2.5rem;
    padding-top: 1.2rem;
    background: rgba(30,34,54,0.7);
    border-radius: 0 0 18px 18px;
    box-shadow: 0 -2px 12px rgba(0,0,0,0.08);
}
</style>
<div class="animated-gradient-box">
    <div style="text-align: center;">
        <span class="pulse-icon"><i class="fa-solid fa-search" style="color: #ff6b6b; font-size: 1.7rem;"></i></span>
        <span class="gradient-title">Find Your Next Favorite Movie</span>
        <div class="fadein-subtitle">Enter any movie title and discover similar films you'll love</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Fix accessibility: provide a non-empty label and hide it
movie_input = st.text_input(
    "Movie Title",  # Non-empty label for accessibility
    value=st.session_state.search_movie,
    placeholder="🎬 Type a movie title (e.g., Inception, Avengers, The Matrix)...",
    help="Enter any movie title to get AI-powered recommendations!",
    key="movie_input",
    label_visibility="collapsed"
)

# --- Add quick suggestions
st.markdown("""
<div style="text-align: center; margin-top: 1rem;">
    <p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 0.6rem;">
        💡 Popular searches:
    </p>
    <div style="display: flex; justify-content: center; gap: 0.5rem; flex-wrap: wrap;">
        <span style="background: rgba(255, 107, 107, 0.2); color: #ff6b6b; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem;">Sci-Fi</span>
        <span style="background: rgba(78, 205, 196, 0.2); color: #4ecdc4; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem;">Action</span>
        <span style="background: rgba(69, 183, 209, 0.2); color: #45b7d1; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem;">Drama</span>
        <span style="background: rgba(150, 206, 180, 0.2); color: #96ceb4; padding: 0.3rem 0.8rem; border-radius: 15px; font-size: 0.8rem;">Thriller</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- Results section ---
if st.session_state.trigger_search:
    st.session_state.trigger_search = False
    movie_to_search = st.session_state.search_movie
else:
    movie_to_search = movie_input
    st.session_state.search_movie = movie_input
    
if movie_to_search.strip():
    # Only show loading animation while waiting for results
    with st.spinner(''):
        results = get_recommendations(movie_to_search, num=6)
    if not results:
        st.markdown("""
        <div class="results-glass">
            <div style="
                background: rgba(244, 67, 54, 0.1);
                border: 1px solid rgba(244, 67, 54, 0.3);
                border-radius: 15px;
                padding: 2rem;
                text-align: center;
                margin: 2rem 0;
            ">
                <i class="fa-solid fa-film-slash" style="font-size: 3rem; color: #f44336; margin-bottom: 1rem;"></i>
                <h3 style="color: #f44336; margin-bottom: 0.5rem;">Movie Not Found</h3>
                <p style="color: #b8c6db;">Sorry, we couldn't find "<strong>{}</strong>" in our database. Please try another title!</p>
                <p style="color: #94a3b8; font-size: 0.9rem; margin-top: 1rem;">💡 Try popular movies like "Inception", "The Matrix", or "Avatar"</p>
            </div>
        </div>
        """.format(movie_to_search), unsafe_allow_html=True)
    else:
        # Success message
        st.markdown(f"""
        <div class="results-glass success-message">
            <i class="fa-solid fa-check-circle" style="margin-right: 8px;"></i>
            <strong>Found {len(results)} amazing movies similar to "{movie_to_search}"!</strong>
        </div>
        """, unsafe_allow_html=True)
        # Display movie recommendations in cards
        st.markdown("<div class='results-glass'>", unsafe_allow_html=True)
        st.markdown("### 🎯 <span style='font-weight:700;'>Your Personalized Recommendations</span>", unsafe_allow_html=True)
        cols = st.columns(2)
        for i, movie in enumerate(results):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="movie-card">
                    <div class="movie-title">
                        <i class="fa-solid fa-clapperboard"></i>
                        {movie['title']}
                    </div>
                    <div class="movie-overview">
                        {movie['overview'][:250]}{'...' if len(movie['overview']) > 250 else ''}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
else:
    st.warning("⚠️ Please enter a movie title to get recommendations!")

# --- Enhanced Footer ---
st.markdown("<hr style='border-color: rgba(255, 255, 255, 0.1); margin-top: 4rem;'>", unsafe_allow_html=True)
st.markdown("""
<div class='footer'>
    <div style="margin-bottom: 1rem;">
        <i class="fa-solid fa-film" style="font-size: 2rem; color: #ff6b6b;"></i>
    </div>
    <div style="font-size: 1.1rem; margin-bottom: 0.5rem;">
        <strong>Movie Buddy</strong> - Your AI-Powered Film Discovery Platform
    </div>
    <div style="font-size: 0.9rem; opacity: 0.7;">
        Built with ❤️ using Streamlit & Machine Learning | © 2025
    </div>
</div>
""", unsafe_allow_html=True)