# Test Documentation

## test_db.py
This file contains test cases for verifying the MongoDB connection in PopcornPicks.
* **test_negative_mongo_connection**: This test case checks if the system correctly handles a failed connection to MongoDB by providing an invalid MongoDB URI. The test ensures that an appropriate error message is returned when the connection fails.

## test_util.py
This file contains test cases for various utility functions used in PopcornPicks, including email notifications, user account management, and movie-related functionalities.
* **test_create_colored_tags**: Verifies that HTML tags with specific colors are correctly generated for different movie genres.
* **test_beautify_feedback_data**: Tests the organization of user feedback data into categories like "Liked", "Disliked", and "Yet to Watch".
* **test_create_movie_genres**: Ensures that a dictionary of movie titles and their associated genres is correctly created from a dataset.
* **test_send_email_to_user**: Checks if an email containing categorized movie feedback is successfully sent to the user.
* **test_create_account**: Tests the creation of a new user account in the database.
* **test_login_to_account**: Verifies both successful and unsuccessful login attempts for users.
* **test_get_username**: Ensures that the correct username is retrieved based on a user ID.
* **test_add_friend_and_get_friends**: Tests adding friends to a user's account and retrieving the list of friends.
* **test_submit_review**: Verifies that users can submit reviews for movies.
* **test_get_wall_posts**: Checks if wall posts (movie reviews) are correctly retrieved for display.
* **test_get_user_history**: Ensures that a user's movie-watching history is correctly retrieved from the database.
* **test_fetch_streaming_link**: Tests fetching streaming links for movies from external APIs.

## test_predict.py
This file contains test cases for checking the functionality of PopcornPicks' recommendation system.
* **test_empty_input**: Verifies that when no input is provided, the recommender returns an empty list of recommendations.
* **test_no_matching_movie**: Tests if the system correctly handles cases where no matching movie is found in the database for a given input.
* **test_duplicate_movies**: Ensures that duplicate movies in the input do not affect the recommendation results.
* **test_genre_similarity_calculation**: Checks whether genre similarity is accurately calculated when generating recommendations based on input movies.
* **test_runtime_similarity_calculation**: Verifies that runtime similarity between movies is considered when making recommendations.
* **test_large_history_input**: Tests how well the recommendation system handles large input histories, ensuring it returns a manageable number of recommendations (up to 10).
* **test_genre_diversity_in_recommendations**: Ensures that recommendations include a diverse range of genres based on user input.

## test_search.py
This file contains test cases for verifying the search functionality in PopcornPicks. The tests ensure that search results are relevant and accurate based on different input queries.
* **test_search_toy**: This test checks if searching for "toy" returns relevant movie titles such as *Toy Story (1995)* and *Toy Story 2 (1999)* in the top 10 results.
* **test_search_love**: This test verifies that searching for "love" returns movies with titles containing "Love", such as *Love & Human Remains (1993)* and *Love Jones (1997)*. The top 10 results should match expected responses.
* **test_search_gibberish**: This test ensures that searching for an irrelevant or nonsensical term like "gibberish" returns an empty result set, as no matching movies should be found.
* **test_search_1995**: This test checks if searching for "1995" returns movies released in 1995, such as *Toy Story (1995)* and *Jumanji (1995)*, ensuring accuracy in year-based search queries.