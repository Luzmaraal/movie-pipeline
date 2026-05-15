import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("TMDB_API_KEY")

GENRE_MAP = {
    28: "Action", 12: "Adventure", 16: "Animation",
    35: "Comedy", 80: "Crime", 99: "Documentary",
    18: "Drama", 10751: "Family", 14: "Fantasy",
    36: "History", 27: "Horror", 10402: "Music",
    9648: "Mystery", 10749: "Romance", 878: "Sci-Fi",
    10770: "TV Movie", 53: "Thriller", 10752: "War",
    37: "Western"
}

def fetch_movies():
    print("Fetching movies from TMDB...")
    movies = []

    for page in range(1, 6):
        url = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&page={page}"
        response = requests.get(url)
        data = response.json()
        movies.extend(data["results"])
        print(f"Fetched page {page} - {len(data['results'])} movies")

    df = pd.DataFrame(movies)

    # Convert genre_ids to genre names
    df["genres"] = df["genre_ids"].apply(
        lambda ids: ", ".join([GENRE_MAP.get(i, "Unknown") for i in ids])
    )

    df = df[[
        "id", "title", "release_date", "popularity",
        "vote_average", "vote_count", "overview", "genres"
    ]]

    print(f"\n✅ Total movies fetched: {len(df)}")
    print(df.head())
    return df

if __name__ == "__main__":
    fetch_movies()