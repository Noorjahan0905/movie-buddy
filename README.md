# 🎬 Movie Buddy

**Movie Buddy** is an AI-powered movie recommendation app built using Streamlit and machine learning techniques. Just enter a movie title, and Movie Buddy finds similar films you'll love.

## 🚀 Features

- 🔍 Intelligent search based on TF-IDF and cosine similarity
- 🖼 Movie poster integration via TMDb API
- 🎨 Modern UI with animations and dark theme
- 💡 Popular suggestions & genre tags

## 🧠 How It Works

1. TF-IDF vectorization of movie overviews
2. Cosine similarity to find related movies
3. Movie metadata from the TMDb dataset/API

## 📁 Dataset

This app uses the TMDb 5000 movie dataset from Kaggle. You can download it here:

- [tmdb_5000_movies.csv](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata/data?select=tmdb_5000_movies.csv)
- [tmdb_5000_credits.csv](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata/data?select=tmdb_5000_credits.csv)

Upload both CSVs to the project directory before running the app.

## 🛠 Tech Stack

- Python
- Streamlit
- Scikit-learn
- TMDb API
- Pandas & NumPy

## 📦 Installation

```bash
git clone https://github.com/<your-username>/movie-buddy.git
cd movie-buddy
pip install -r requirements.txt
streamlit run app.py
