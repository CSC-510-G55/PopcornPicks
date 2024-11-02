Here's the content formatted in markdown:

# app.py

### login_page()
Renders the login page of the web-app.

### profile_page()
Renders the profile page of the web-app.
Fetches genre count for the user from the database.

### wall_page()
Renders the wall page of the web-app.
Checks if the user is logged in or a guest before rendering.

### review_page()
Renders the review page of the web-app.
Ensures user is logged in or a guest before rendering.

### landing_page()
Renders the landing page of the web-app.
Ensures user is logged in or a guest before rendering.

### search_page()
Renders the search page of the web-app.
Ensures user is logged in or a guest before rendering.

### predict()
Predicts movie recommendations based on user-input movies.
* Input: List of movies rated by the user.
* Output: Recommended movies, genres, IMDb IDs, and streaming links.

### search()
Handles movie search requests.
* Input: Search term.
* Output: Top 10 movie results matching the search term.

### create_acc()
Handles creating a new account.
* Input: User data (email, username, password).
* Output: Creates a new account in the database.

### signout()
Handles signing out of the active user.
Resets user session data.

### login()
Handles logging in an active user.
* Input: Username and password.
* Output: User session is set if credentials are valid.

### friend()
Handles adding a new friend to the user's account.
* Input: Friend's username.
* Output: Adds friend to user's friend list in the database.

### guest()
Sets the current session to guest mode.
* Input: Guest identifier.
* Output: User session is set as guest.

### review()
Handles submission of a movie review by a user.
* Input: Movie title, score, and review text.
* Output: Saves review data to the database.

### wall_posts()
Fetches posts for the user's wall.
* Output: List of recent posts from friends and other users.

### recent_movies()
Gets recent movies rated by the active user.
* Output: List of recently rated movies by the logged-in user.

### recent_friend_movies()
Gets recent movies rated by a specific friend.
* Input: Friend's ID.
* Output: List of recently rated movies by that friend.

### username()
Fetches username of the active user.
* Output: Username associated with the current session's user ID.

### get_friend()
Fetches friends of the active user.
* Output: List of friends associated with the current user's account.

### feedback()
Handles submission of feedback from users and sends it via email.
* Input: Feedback data.
* Output: Sends feedback email to user's registered email address.

### send_mail()
Handles sending emails with feedback or recommendations to users.
* Input: Recipient email and feedback data.
* Output: Sends email with categorized movie recommendations or feedback details.

### success()
Renders success page after successful operations like account creation or feedback submission.

### before_request()
Opens a connection to the database before processing each request.

### after_request()
Closes database connection after processing each request.

# item_based.py

### load_movies()
Loads movie data from CSV file into a DataFrame.

### prepare_ratings(db)
Prepares ratings DataFrame from database records.
* Input: Database connection.
* Output: DataFrame containing user ratings (user_id, movie_id, score).

### prepare_surprise_df(ratings)
Prepares DataFrame for use with Surprise library (collaborative filtering).
* Input: Ratings DataFrame.
* Output: DataFrame formatted for Surprise library (user, item, rating).

### generate_cf_recommendations(surprise_df, ratings, movies, user_id)
Generates collaborative filtering recommendations using SVD model for a specific user.
* Input: Surprise-formatted DataFrame, ratings DataFrame, movies DataFrame, and user ID.
* Output: List of recommended movie IDs and their predicted ratings.

### calculate_genre_similarity(selected_movies, enriched_movies)
Calculates genre similarity between selected movies and all other movies based on genres.

### calculate_runtime_similarity(selected_movies, enriched_movies)
Calculates runtime similarity between selected movies and all other movies based on runtime duration.

### calculate_hybrid_score(enriched_movies, user_rating_count)
Calculates hybrid score for recommendations using weights for genre similarity, collaborative filtering predictions, and runtime similarity based on user's rating count.

### recommend_for_new_user(user_rating, user_id, db)
Generates recommendations for new users based on their initial ratings using collaborative filtering and genre/runtime similarity analysis.
* Input: User's initial ratings (list), User ID, Database connection.
* Output: Recommended movie titles, genres, IMDb IDs for top 10 recommended movies.

# utils.py

### load_movies()
Loads movie data from CSV file into a DataFrame for further processing or analysis.

### create_colored_tags(genres)
Generates HTML tags with colors corresponding to different movie genres for display purposes.
* Input: List of genres.
* Output: String containing HTML tags with appropriate colors for each genre.

### beautify_feedback_data(data)
Formats feedback data into categories (Liked, Disliked, Yet to Watch) for sending in emails or display purposes.
* Input: Feedback data dictionary (movie titles mapped to status).
* Output: Categorized dictionary with lists of liked/disliked/yet-to-watch movies.

### create_movie_genres(movie_genre_df)
Creates a dictionary mapping each movie title to its respective genres from a DataFrame containing movie information.

### send_email_to_user(recipient_email, categorized_data)
Sends an email containing categorized movie recommendations or feedback to a specified recipient email address using SMTP protocol.

# search.py

### starts_with(word)
Searches for movies whose titles start with a given prefix (case-insensitive).
* Input: Search word/prefix.
* Output: List of matching movie titles starting with that prefix.

### anywhere(word, visited_words)
Searches for movies whose titles contain a given word but have not been visited yet (case-insensitive).
* Input: Search word and list of already visited words/titles.
* Output: List of matching movie titles that contain the word but haven't been visited yet.

### results(word)
Combines results from both starts_with and anywhere methods to return all matching titles for a given word/prefix (case-insensitive).

### results_top_ten(word)
Returns only top 10 results from results() method based on search word/prefix (case-insensitive).