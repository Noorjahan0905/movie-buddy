# 🎬 Movie Buddy

**Movie Buddy** is an AI-powered movie recommendation app built using Streamlit and machine learning techniques. Just enter a movie title, and Movie Buddy finds similar films you'll love.

movie-buddy/
├── app.py
├── recommender.py   # assumed dependency, create or add yours
├── .gitignore
├── README.md
├── LICENSE
└── .github/
    └── workflows/
        └── deploy.yml

## 🚀 Features

- 🔍 Intelligent search based on TF-IDF and cosine similarity
- 🖼 Movie poster integration via TMDb API
- 🎨 Modern UI with animations and dark theme
- 💡 Popular suggestions & genre tags

## 🧠 How It Works

1. TF-IDF vectorization of movie overviews
2. Cosine similarity to find related movies
3. Movie metadata from the TMDb dataset/API

## 🛠 Tech Stack

- Python
- Streamlit
- Scikit-learn / NLP
- TMDb API

## 📦 Installation

```bash
git clone https://github.com/<your-username>/movie-buddy.git
cd movie-buddy
pip install -r requirements.txt
streamlit run app.py
