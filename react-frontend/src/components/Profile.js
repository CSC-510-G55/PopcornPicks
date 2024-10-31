import React, { useState, useEffect } from 'react';
import axios from 'axios';
import '../ProfilePage.css';
// import '../stylesheet.css';

const ProfilePage = () => {
  const [userName, setUserName] = useState('');
  const [userMovies, setUserMovies] = useState([]);
  const [friends, setFriends] = useState([]);
  const [newFriend, setNewFriend] = useState('');

  useEffect(() => {
    getUserName();
    getRecentMoviesProfile();
    getFriends();
  }, []);

  const getUserName = async () => {
    try {
      const response = await axios.get('/getUserName');
      setUserName(response.data);
    } catch (error) {
      console.error('Error fetching user name:', error);
    }
  };

  const getRecentMoviesProfile = async () => {
    try {
      const response = await axios.get('/getRecentMovies');
      console.log(response.data);
      
      // Assuming the response is an array of objects with a "movie" property
      setUserMovies(response.data);
    } catch (error) {
      console.error('Error fetching recent movies:', error);
    }
  };

  const getFriends = async () => {
    try {
      const response = await axios.get('/getFriends');
      
      const friendsData = response.data;
      console.log(friendsData);
      
      const friendsWithMovies = await Promise.all(
        friendsData.map(async (friend) => {
          const moviesResponse = await axios.post('/getRecentFriendMovies', {"friend_id": friend}, {
            headers: { 'Content-Type': 'application/json' }
          });
          console.log(moviesResponse);
          
          return { 
            _id: friend._id,
            name: friend.username, 
            movies: moviesResponse.data, 
            showMovies: false 
          };
        })
      );
      console.log(friendsWithMovies);
      
      setFriends(friendsWithMovies);
    } catch (error) {
      console.error('Error fetching friends:', error);
    }
  };

  const addFriend = async () => {
    // Implement the logic to add a friend
    console.log('Adding friend:', newFriend);
    setNewFriend('');
  };

  const showFriendMovies = (friendName) => {
    setFriends(friends.map(friend => ({
      ...friend,
      showMovies: friend.name === friendName ? !friend.showMovies : false
    })));
  };

  const backToLandingPage = () => {
    window.location.href = "/landing";
  };

  return (
    <div className="profile-page">
      <h1 id="userNameBanner">Welcome {userName}!</h1>

      <div className="container">
        <div className="section">
          <h2>Your Reviewed Movies</h2>
          <ul id="userMovies">
            {userMovies.map((movie, index) => (
              <li key={index} className="movie">
                {movie.title}: {movie.score}/10 stars
              </li>
            ))}
          </ul>
        </div>

        <div className="section">
          <h2>Your Friends</h2>
          <ul id="friendsList">
            {friends.map((friend, index) => (
              <li key={index} className="friend">
                {friend.name}
                <button onClick={() => showFriendMovies(friend.name)}>
                  {friend.showMovies ? 'Hide Movies' : 'Show Movies'}
                </button>
                {friend.showMovies && (
                  <div className="friend-dropdown">
                    {friend.movies.map((movie, movieIndex) => (
                      <a key={movieIndex}>
                        {movie.name}: {movie.score}/10 stars
                      </a>
                    ))}
                  </div>
                )}
              </li>
            ))}
          </ul>
        </div>
      </div>

      <div>
        <input
          type="text"
          placeholder="Enter Your Friend's Username"
          value={newFriend}
          onChange={(e) => setNewFriend(e.target.value)}
          className="form-control"
        />
        <button onClick={addFriend} className="btn btn-primary">Add Friend</button>
      </div>

      <button onClick={backToLandingPage} className="btn btn-primary">Return home</button>
    </div>
  );
};

export default ProfilePage;