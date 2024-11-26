import pytest
from unittest.mock import MagicMock, patch
from pymongo.errors import DuplicateKeyError, OperationFailure
from backend.recommenderapp.app import app
from backend.recommenderapp.app import setup_mongodb_indexes
from backend.recommenderapp.app import send_email_to_user
from backend.recommenderapp.app import get_friends
from flask import json

# Mock the MongoDB collection objects
@pytest.fixture
def mock_mongo_collections():
    with patch("backend.recommenderapp.app.db.users") as mock_users, \
         patch("backend.recommenderapp.app.db.movies") as mock_movies, \
         patch("backend.recommenderapp.app.db.ratings") as mock_ratings:

        # Mocking the `create_index` method for all collections
        mock_users.create_index = MagicMock()
        mock_movies.create_index = MagicMock()
        mock_ratings.create_index = MagicMock()

        # Returning the mocked collections
        yield mock_users, mock_movies, mock_ratings


def test_setup_mongodb_indexes(mock_mongo_collections):
    """
    Test the setup_mongodb_indexes function to ensure indexes are created correctly.
    """
    mock_users, mock_movies, mock_ratings = mock_mongo_collections

    # Call the function to setup indexes
    setup_mongodb_indexes()

    # Assert that the `create_index` method was called with the correct parameters
    mock_users.create_index.assert_any_call([("username", 1)])
    mock_users.create_index.assert_any_call([("email", 1)])

    mock_movies.create_index.assert_any_call([("imdb_id", 1)], unique=True)
    mock_movies.create_index.assert_any_call([("name", 1)])

    mock_ratings.create_index.assert_any_call([("user_id", 1), ("time", -1)])
    mock_ratings.create_index.assert_any_call([("movie_id", 1)])


def test_setup_mongodb_indexes_duplicate_key_error(mock_mongo_collections):
    """
    Test handling of DuplicateKeyError when creating indexes.
    """
    mock_users, mock_movies, mock_ratings = mock_mongo_collections

    # Simulate DuplicateKeyError when creating the index
    mock_users.create_index.side_effect = DuplicateKeyError("Duplicate key error")

    # Call the function and ensure that the error is handled
    with patch("builtins.print") as mock_print:
        setup_mongodb_indexes()

        # Check that the error message is printed
        mock_print.assert_called_with("Duplicate key error: Duplicate key error")


def test_setup_mongodb_indexes_operation_failure(mock_mongo_collections):
    """
    Test handling of OperationFailure when creating indexes.
    """
    mock_users, mock_movies, mock_ratings = mock_mongo_collections

    # Simulate OperationFailure when creating the index
    mock_users.create_index.side_effect = OperationFailure("Operation failed")

    # Call the function and ensure that the error is handled
    with patch("builtins.print") as mock_print:
        setup_mongodb_indexes()

        # Check that the error message is printed
        mock_print.assert_called_with("Operation failed: Operation failed")


def test_setup_mongodb_indexes_successful_creation(mock_mongo_collections):
    """
    Test that indexes are created successfully and a success message is printed.
    """
    mock_users, mock_movies, mock_ratings = mock_mongo_collections

    # Call the function to setup indexes
    with patch("builtins.print") as mock_print:
        setup_mongodb_indexes()

        # Ensure that a success message is printed
        mock_print.assert_called_with("Indexes created successfully")


def test_create_index_called_once(mock_mongo_collections):
    """
    Test that create_index is called exactly once per unique index.
    """
    mock_users, mock_movies, mock_ratings = mock_mongo_collections

    # Call the function to setup indexes
    setup_mongodb_indexes()

    # Verify that `create_index` is called exactly once for each unique index
    assert mock_users.create_index.call_count == 2  # username, email
    assert mock_movies.create_index.call_count == 2  # imdb_id, name
    assert mock_ratings.create_index.call_count == 2  # user_id, time, movie_id

# Mock the db and user
@pytest.fixture
def mock_db_and_user():
    with patch("backend.recommenderapp.app.db") as mock_db:
        mock_db.users.find_one = MagicMock(return_value={"email": "testuser@example.com"})
        yield mock_db  # This is the mocked db instance

# Test for /getFriends route
def test_get_friends(mock_db_and_user):
    """
    Test the /getFriends route to ensure the friends of the user are fetched.
    """
    with app.test_client() as client:
        # Mock the get_friends function to return some sample friends
        with patch("backend.recommenderapp.app.get_friends") as mock_get_friends:
            mock_get_friends.return_value = ["friend1", "friend2", "friend3"]
            
            # Call the /getFriends route
            response = client.get("/getFriends")
            
            # Assert that get_friends was called with the correct parameters
            mock_get_friends.assert_called_with(mock_db_and_user, "673e820d3f9e32b77366db00")  # Hardcoded user ID

            # Assert that the response is correct
            assert response.status_code == 200
            assert response.json == ["friend1", "friend2", "friend3"]

def test_get_friends_no_friends(mock_db_and_user):
    """
    Test the /getFriends route when the user has no friends.
    """
    with app.test_client() as client:
        with patch("backend.recommenderapp.app.get_friends") as mock_get_friends:
            # Simulate no friends
            mock_get_friends.return_value = []
            
            # Call the /getFriends route
            response = client.get("/getFriends")
            
            # Assert that get_friends was called with the correct parameters
            mock_get_friends.assert_called_with(mock_db_and_user, "673e820d3f9e32b77366db00")
            
            # Assert that the response is an empty list
            assert response.status_code == 200
            assert response.json == []

def test_get_friends_db_failure(client):
    # Simulate a database failure (mock the function to raise an exception)
    with patch("backend.recommenderapp.app.get_friends", side_effect=Exception("Database error")):
        # Act: Call the /getFriends route
        response = client.get("/getFriends")
        
        # Assert: Check that the response is 500 Internal Server Error
        assert response.status_code == 500

#Test with an invalid user ID (e.g., invalid session or corrupted data)
def test_invalid_user_id(client):
    # Simulate an invalid user ID scenario
    with patch("backend.recommenderapp.app.get_friends") as mock_get_friends:
        # Simulate a corrupted or invalid user ID that would cause failure in the database query
        mock_get_friends.side_effect = Exception("Invalid user ID")
        
        # Act: Call the /getFriends route
        response = client.get("/getFriends")
        
        # Assert: Ensure the server returns a 400 or 500 error with an appropriate message
        assert response.status_code == 500

#Test when get_friends function returns a large list of friends
def test_large_number_of_friends(client):
    # Simulate a user with 100 friends
    friends_list = [f"friend{i}" for i in range(1, 101)]  # List of 100 friends
    
    with patch("backend.recommenderapp.app.get_friends") as mock_get_friends:
        mock_get_friends.return_value = friends_list  # Return 100 friends
        
        # Act: Call the /getFriends route
        response = client.get("/getFriends")
        
        # Assert: Ensure the response is correct and handles a large list
        assert response.status_code == 200
        assert len(response.json) == 100  # Ensure 100 friends are returned
        assert "friend1" in response.json  # Check the first friend is included
        assert "friend100" in response.json  # Check the last friend is included


# Test for /feedback route
def test_feedback(mock_db_and_user):
    """
    Test the /feedback route to ensure feedback is processed and an email is sent.
    """
    # Example of feedback data that might be passed to beautify_feedback_data
    feedback_data = {
        "Liked": [],
        "Disliked": [],
        "Yet to Watch": []
    }

    # Mock the beautify_feedback_data function to return the expected structure
    with app.test_client() as client:
        with patch("backend.recommenderapp.app.send_email_to_user") as mock_send_email:
            with patch("backend.recommenderapp.app.beautify_feedback_data", return_value=feedback_data):
                # Simulate the request
                response = client.post("/feedback", json={
                    "message": "Amazing app!",
                    "rating": 5
                })
                
                # Ensure the email function is called with the correct processed data
                mock_send_email.assert_called_with("testuser@example.com", feedback_data)
                
                # Check that the response is correct (return the data)
                assert response.status_code == 200
                assert response.json == {"message": "Amazing app!", "rating": 5}


#Test when the email sending fails
def test_feedback_email_failure(client):
    # Example feedback data
    feedback_data = {
        "message": "Amazing app!",
        "rating": 5
    }

    # Simulate the case where sending email fails (raise an exception)
    with patch("backend.recommenderapp.app.send_email_to_user", side_effect=Exception("Email send failed")):
        with patch("backend.recommenderapp.app.beautify_feedback_data", return_value=feedback_data):
            # Act: Send feedback
            response = client.post("/feedback", json=feedback_data)

            # Assert: Check if an error message is returned, since email failed
            assert response.status_code == 500

#Test when the beautify_feedback_data function raises an exception
def test_beautify_feedback_data_failure(client):
    # Simulate an exception raised in beautify_feedback_data
    feedback_data = {
        "message": "Amazing app!",
        "rating": 5
    }

    with patch("backend.recommenderapp.app.beautify_feedback_data", side_effect=Exception("Invalid feedback data")):
        # Act: Send the feedback request
        response = client.post("/feedback", json=feedback_data)

        # Assert: Check that the error is handled and the server returns a 500 error
        assert response.status_code == 500

def test_send_mail():
    """
    Test the /sendMail route to ensure feedback is sent to the given email address.
    """
    # Example of feedback data that might be passed to beautify_feedback_data
    feedback_data = {
        "Liked": [],
        "Disliked": [],
        "Yet to Watch": []
    }

    # Mock the beautify_feedback_data function to return the expected structure
    with app.test_client() as client:
        with patch("backend.recommenderapp.app.send_email_to_user") as mock_send_email:
            with patch("backend.recommenderapp.app.beautify_feedback_data", return_value=feedback_data):
                # Simulate the request
                response = client.post("/sendMail", json={
                    "email": "user@example.com",
                    "message": "Amazing app!",
                    "rating": 5
                })
                
                # Ensure the email function is called with the correct processed data
                mock_send_email.assert_called_with("user@example.com", feedback_data)
                
                # Check that the response is correct (return the data)
                assert response.status_code == 200
                assert response.json == {"email": "user@example.com", "message": "Amazing app!", "rating": 5}


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@patch("backend.recommenderapp.app.get_username")  # Mock the get_username function
def test_username_route(mock_get_username, client):
    # Arrange: Define the mock return value for get_username
    mock_get_username.return_value = "test_user"

    # Act: Make a GET request to the /getUserName route
    response = client.get("/getUserName")

    # Assert: Check that the response is as expected
    assert response.status_code == 200  # HTTP status code 200 means OK
    assert response.data == b'test_user'  # The response should be the username "test_user"

@patch("backend.recommenderapp.app.get_username")  # Mock the get_username function
def test_username_empty(mock_get_username, client):
    # Arrange: Simulate that the username is an empty string
    mock_get_username.return_value = ""

    # Act: Make a GET request to the /getUserName route
    response = client.get("/getUserName")

    # Assert: Check that the response returns an empty string for the username
    assert response.status_code == 200
    assert response.data == b''  # The response should be an empty username

@patch("backend.recommenderapp.app.get_username")  # Mock the get_username function
def test_username_db_failure(mock_get_username, client):
    # Arrange: Simulate a database failure (e.g., an exception thrown while querying the database)
    mock_get_username.side_effect = Exception("Database connection error")

    # Act: Make a GET request to the /getUserName route
    response = client.get("/getUserName")

    # Assert: Ensure that the response indicates a server error
    assert response.status_code == 500  # HTTP status code for internal server error