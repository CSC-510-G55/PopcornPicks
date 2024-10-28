"""
Copyright (c) 2024 Srimadh Vasuki Rao, Manav Shah, Akul Devali
This code is licensed under MIT license (see LICENSE for details)

@author: PopcornPicks
"""

import os
import pandas as pd
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
import sys

sys.path.append("../")
from src.recommenderapp.utils import get_user_ratings

sys.path.remove("../")
import json

app_dir = os.path.dirname(os.path.abspath(__file__))
code_dir = os.path.dirname(app_dir)
project_dir = os.path.dirname(code_dir)


from surprise import Dataset, Reader, SVD
import pandas as pd
import numpy as np
import os


def recommend_for_new_user(user_rating, user_id, client):
    """
    Generates a list of recommended movie titles for a new user using a hybrid approach:
    collaborative filtering based on user history combined with metadata matching with current selection.
    """
    if not user_rating:
        return [],None,None
    movies = pd.read_csv(os.path.join(project_dir, "data", "movies.csv"))

    all_ratings = get_user_ratings(client)

    ratings = pd.DataFrame(all_ratings)
    ratings["user_id"] = ratings["user_id"].astype(str)
    ratings["movie_id"] = ratings["movie_id"].astype(str)
    surprise_df = ratings[["user_id", "movie_id", "score"]].copy()
    surprise_df.columns = ["user", "item", "rating"]

    surprise_df["user"] = surprise_df["user"].apply(
        lambda x: int(x, 16) if pd.notnull(x) else None
    )
    surprise_df["item"] = surprise_df["item"].astype(str).astype(int)

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

    recommendations_df = pd.DataFrame(
        recommendations, columns=["movieId", "predicted_rating"]
    )
    enriched_movies = pd.merge(recommendations_df, movies, on="movieId")

    selected_movies = movies[
        movies["title"].isin([movie["title"] for movie in user_rating])
    ]

    avg_genre_vector = selected_movies["genres"].str.get_dummies(sep="|").mean()

    enriched_movies_genres = enriched_movies["genres"].str.get_dummies(sep="|")
    enriched_movies_genres = enriched_movies_genres.reindex(
        columns=avg_genre_vector.index, fill_value=0
    )

    enriched_movies["genre_similarity"] = enriched_movies_genres.dot(avg_genre_vector)

    avg_runtime = selected_movies["runtime"].mean()

    enriched_movies["runtime_similarity"] = (
        1
        - abs(enriched_movies["runtime"] - avg_runtime)
        / enriched_movies["runtime"].max()
    )

    if len(ratings[ratings["user_id"] == user_id]) < 10:
        user_rating_weight = 1
        collaborative_weight = 0
        genre_weight = 0
    else:
        user_rating_weight = 0.5
        collaborative_weight = 0.4
        genre_weight = 0.1

    enriched_movies["hybrid_score"] = (
        user_rating_weight * enriched_movies["genre_similarity"]
        + collaborative_weight * enriched_movies["predicted_rating"]
        + genre_weight * enriched_movies["runtime_similarity"]
    )

    enriched_movies.sort_values(by="hybrid_score", ascending=False, inplace=True)

    top_movies = enriched_movies.head(10)

    return (
        list(top_movies["title"]),
        list(top_movies["genres"]),
        list(top_movies["imdb_id"]),
    )
