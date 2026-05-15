from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
import pandas as pd
import psycopg2
import os

API_KEY = os.getenv("TMDB_API_KEY", "your_api_key_here")

GENRE_MAP = {
    28: "Action", 12: "Adventure", 16: "Animation",
    35: "Comedy", 80: "Crime", 99: "Documentary",
    18: "Drama", 10751: "Family", 14: "Fantasy",
    36: "History", 27: "Horror", 10402: "Music",
    9648: "Mystery", 10749: "Romance", 878: "Sci-Fi",
    10770: "TV Movie", 53: "Thriller", 10752: "War",
    37: "Western"
}

def fetch_and_load():
    print("Fetching movies from TMDB...")
    movies = []
    for page in range(1, 6):
        url = f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&page={page}"
        response = requests.get(url)
        data = response.json()
        movies.extend(data["results"])
        print(f"Fetched page {page}")

    df = pd.DataFrame(movies)
    df["genres"] = df["genre_ids"].apply(
        lambda ids: ", ".join([GENRE_MAP.get(i, "Unknown") for i in ids])
    )
    df = df[["id", "title", "release_date", "popularity",
             "vote_average", "vote_count", "overview", "genres"]]

    print("Connecting to database...")
    conn = psycopg2.connect(
        host="postgres",
        port="5432",
        database="airflow",
        user="airflow",
        password="airflow"
    )
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS movies")
    cursor.execute("""
        CREATE TABLE movies (
            id INTEGER PRIMARY KEY,
            title VARCHAR(255),
            release_date VARCHAR(50),
            popularity FLOAT,
            vote_average FLOAT,
            vote_count INTEGER,
            overview TEXT,
            genres VARCHAR(255)
        )
    """)
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO movies 
                (id, title, release_date, popularity, vote_average, vote_count, overview, genres)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, tuple(row))
    conn.commit()
    conn.close()
    print(f"✅ {len(df)} movies loaded successfully!")

with DAG(
    dag_id='movie_pipeline',
    description='Fetches movies from TMDB and loads into PostgreSQL',
    schedule_interval=None,
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['movies', 'tmdb', 'portfolio']
) as dag:

    task_fetch_and_load = PythonOperator(
        task_id='fetch_and_load_movies',
        python_callable=fetch_and_load
    )