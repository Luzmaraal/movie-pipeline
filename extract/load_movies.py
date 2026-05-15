import psycopg2
import os
from dotenv import load_dotenv
from fetch_movies import fetch_movies

load_dotenv()

def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        port="5433",
        database="airflow",
        user="airflow",
        password="airflow"
    )
    return conn

def create_table(conn):
    cursor = conn.cursor()
    # Drop old table and recreate with genres column
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
    conn.commit()
    print("✅ Table created successfully!")

def load_movies_to_db(conn, df):
    cursor = conn.cursor()
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO movies 
                (id, title, release_date, popularity, vote_average, vote_count, overview, genres)
            VALUES 
                (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, (
            row["id"],
            row["title"],
            row["release_date"],
            row["popularity"],
            row["vote_average"],
            row["vote_count"],
            row["overview"],
            row["genres"]
        ))
    conn.commit()
    print(f"✅ {len(df)} movies loaded into the database!")

def main():
    print("Connecting to database...")
    conn = get_db_connection()
    print("Creating table...")
    create_table(conn)
    print("Fetching movies from TMDB...")
    df = fetch_movies()
    print("Loading movies into database...")
    load_movies_to_db(conn, df)
    conn.close()
    print("✅ Done!")

if __name__ == "__main__":
    main()