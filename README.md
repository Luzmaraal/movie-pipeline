# 🎬 CineStats — Movie Analytics Pipeline

An end-to-end data engineering pipeline that fetches real movie data from TMDB, stores it in PostgreSQL, transforms it with dbt, orchestrates it with Airflow, and visualizes it in Tableau.

---

## 🏗️ Architecture
---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Data extraction & loading |
| PostgreSQL | Data storage |
| dbt | Data transformation |
| Apache Airflow | Pipeline orchestration |
| Docker | Containerization |
| Tableau Public | Data visualization |

---

## 📊 Dashboard

👉 [View the CineStats Dashboard on Tableau Public] 
https://public.tableau.com/app/profile/luz4034/viz/CineStats-MovieAnalytics/CineStats-MovieAnalytics?publish=yes

---

## 🚀 How to Run This Project

### Prerequisites
- Docker Desktop
- Python 3.8+
- dbt-postgres

### 1. Clone the repository
```bash
git clone https://github.com/Luzmaraal/movie-pipeline.git
cd movie-pipeline
```

### 2. Create your .env file
```bash
touch .env
```
Add your TMDB API key:

### 3. Start Docker services
```bash
docker compose up -d
```

### 4. Install Python dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install pandas requests psycopg2-binary python-dotenv
```

### 5. Run the pipeline
```bash
python extract/load_movies.py
```

### 6. Run dbt transformations
```bash
cd movie_transforms
dbt run
```

### 7. Or trigger via Airflow
Go to http://localhost:8080 and trigger the `movie_pipeline` DAG

---

## 📁 Project Structure

---

## 🔄 Pipeline Steps

1. **Extract** — Python fetches 100 popular movies from TMDB API
2. **Load** — Data is stored in PostgreSQL running in Docker
3. **Transform** — dbt creates clean analytical tables
4. **Visualize** — Tableau Public dashboard displays insights
5. **Orchestrate** — Airflow manages and monitors the pipeline

---

## 👩🏻‍💻 Author

Built by Luz Ramirez as a data engineering portfolio project.

Connect with me on [LinkedIn]https://www.linkedin.com/in/luz-ramirez-b41828a9/ ← add your LinkedIn here