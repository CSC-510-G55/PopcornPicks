"""
Copyright (c) 2024 Srimadh Vasuki Rao, Manav Shah, Akul Devali
This code is licensed under MIT license (see LICENSE for details)

@author: PopcornPicks
"""

import os
import pandas as pd
from surprise import Dataset, Reader, SVD
from src.recommenderapp.utils import get_user_ratings

app_dir = os.path.dirname(os.path.abspath(__file__))
code_dir = os.path.dirname(app_dir)
project_dir = os.path.dirname(code_dir)


def load_movies():
    """Load movies data from CSV."""
    return pd.read_csv(os.path.join(project_dir, "data", "movies.csv"))


def prepare_ratings(db):
    """Prepare ratings DataFrame."""
    all_ratings = get_user_ratings(db)
    ratings = pd.DataFrame(all_ratings)
    ratings["user_id"] = ratings["user_id"].astype(str)
    ratings["movie_id"] = ratings["movie_id"].astype(str)
    return ratings


def prepare_surprise_df(ratings):
    """Prepare DataFrame for Surprise library."""
    surprise_df = ratings[["user_id", "movie_id", "score"]].copy()
    surprise_df.columns = ["user", "item", "rating"]
    surprise_df["user"] = surprise_df["user"].apply(
        lambda x: int(x, 16) if pd.notnull(x) else None
    )
    surprise_df["item"] = surprise_df["item"].astype(str).astype(int)
    return surprise_df


def generate_cf_recommendations(surprise_df, ratings, movies, user_id):
    """Generate collaborative filtering recommendations."""
    reader = Reader(rating_scale=(0, 10))
    data = Dataset.load_from_df(surprise_df, reader)
    trainset = data.build_full_trainset()
    svd_model = SVD()
    svd_model.fit(trainset)

    user_rated_movies = ratings[ratings["user_id"] == user_id]["movie_id"].tolist()
    all_movie_ids = movies["movieId"].unique()

    recommendations = []
    for movie_id in all_movie_ids:
        if movie_id not in user_rated_movies:
            pred = svd_model.predict(int(user_id, 16), movie_id)
            recommendations.append((movie_id, pred.est))
    return recommendations


def calculate_genre_similarity(selected_movies, enriched_movies):
    """Calculate genre similarity."""
    avg_genre_vector = selected_movies["genres"].str.get_dummies(sep="|").mean()
    enriched_movies_genres = enriched_movies["genres"].str.get_dummies(sep="|")
    enriched_movies_genres = enriched_movies_genres.reindex(
        columns=avg_genre_vector.index, fill_value=0
    )
    enriched_movies["genre_similarity"] = enriched_movies_genres.dot(avg_genre_vector)


def calculate_runtime_similarity(selected_movies, enriched_movies):
    """Calculate runtime similarity."""
    avg_runtime = selected_movies["runtime"].mean()
    enriched_movies["runtime_similarity"] = (
        1
        - abs(enriched_movies["runtime"] - avg_runtime)
        / enriched_movies["runtime"].max()
    )


def calculate_hybrid_score(enriched_movies, user_rating_count):
    """Calculate hybrid score for recommendations."""
    if user_rating_count < 10:
        user_rating_weight, collaborative_weight, genre_weight = 1, 0, 0
    else:
        user_rating_weight, collaborative_weight, genre_weight = 0.5, 0.4, 0.1

    enriched_movies["hybrid_score"] = (
        user_rating_weight * enriched_movies["genre_similarity"]
        + collaborative_weight * enriched_movies["predicted_rating"]
        + genre_weight * enriched_movies["runtime_similarity"]
    )


def recommend_for_new_user(user_rating, user_id, db):
    """Generate recommendations for a new user."""
    if not user_rating:
        return [], None, None
    movies = load_movies()
    ratings = prepare_ratings(db)
    surprise_df = prepare_surprise_df(ratings)

    recommendations = generate_cf_recommendations(surprise_df, ratings, movies, user_id)

    recommendations_df = pd.DataFrame(
        recommendations, columns=["movieId", "predicted_rating"]
    )
    enriched_movies = pd.merge(recommendations_df, movies, on="movieId")

    selected_movies = movies[
        movies["title"].isin([movie["title"] for movie in user_rating])
    ]

    if selected_movies.empty:
        return [], None, None

    calculate_genre_similarity(selected_movies, enriched_movies)
    calculate_runtime_similarity(selected_movies, enriched_movies)
    calculate_hybrid_score(enriched_movies, len(ratings[ratings["user_id"] == user_id]))
    enriched_movies.sort_values(by="hybrid_score", ascending=False, inplace=True)

    top_movies = enriched_movies.head(10)

    return (
        list(top_movies["title"]),
        list(top_movies["genres"]),
        list(top_movies["imdb_id"]),
    )
