import React, { useState, useEffect } from "react";
import axios from "axios";
import "../ProfilePage.css";
import { useNavigate } from "react-router-dom";
// import '../stylesheet.css';

const API_BASE_URL = process.env.REACT_APP_API_URL;

const ProfilePage = () => {
  const [userName, setUserName] = useState("");
  const [userMovies, setUserMovies] = useState([]);
  const [friends, setFriends] = useState([]);
  const [newFriend, setNewFriend] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    getUserName();
    getRecentMoviesProfile();
    getFriends();
  }, []);

  const getUserName = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/getUserName`);
      setUserName(response.data);
    } catch (error) {
      console.error("Error fetching user name:", error);
    }
  };

  const getRecentMoviesProfile = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/getRecentMovies`);
      console.log(response.data);

      // Assuming the response is an array of objects with a "movie" property
      setUserMovies(response.data);
    } catch (error) {
      console.error("Error fetching recent movies:", error);
    }
  };

  const getFriends = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/getFriends`);

      const friendsData = response.data;
      console.log(friendsData);

      const friendsWithMovies = await Promise.all(
        friendsData.map(async (friend) => {
          const moviesResponse = await axios.post(
            `${API_BASE_URL}/getRecentFriendMovies`,
            { friend_id: friend },
            {
              headers: { "Content-Type": "application/json" },
            },
          );
          console.log(moviesResponse);

          return {
            _id: friend._id,
            name: friend.username,
            movies: moviesResponse.data,
            showMovies: false,
          };
        }),
      );
      console.log(friendsWithMovies);

      setFriends(friendsWithMovies);
    } catch (error) {
      console.error("Error fetching friends:", error);
    }
  };
  const handleSignOut = async () => {
    const data = {
      user: "None",
    };

    try {
      const response = await axios.post(`${API_BASE_URL}/out`, data, {
        headers: {
          "Content-Type": "application/json;charset=UTF-8",
        },
      });

      if (response.status === 200) {
        console.log("Signed out successfully");
        // Navigate to the home page after a short delay
        setTimeout(() => {
          navigate("/");
        }, 1000);
      }
    } catch (error) {
      console.error("Sign out error:", error);
    }
  };
  const addFriend = async () => {
    // Implement the logic to add a friend
    try {
      const response = await axios.post(
        `${API_BASE_URL}/friend`,
        { username: newFriend },
        {
          headers: { "Content-Type": "application/json" },
        },
      );

      console.log("Adding friend:", newFriend);
      console.log("Server response:", response.data);

      // Update the friends list in the state
      setFriends((prevFriends) => [...prevFriends, response.data]);

      // Clear the input field
      setNewFriend("");
    } catch (error) {
      console.error("Error adding friend:", error);
    }
    console.log("Adding friend:", newFriend);
  };

  const showFriendMovies = (friendName) => {
    setFriends(
      friends.map((friend) => ({
        ...friend,
        showMovies: friend.name === friendName ? !friend.showMovies : false,
      })),
    );
  };

  const backToLandingPage = () => {
    window.location.href = "/landing";
  };

  return (
    <>
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark topNavBar fixed-top">
        <div className="container-fluid">
          <a className="navbar-brand" href="/landing">
            PopcornPicks🍿
          </a>
          <button
            type="button"
            id="signOut"
            onClick={handleSignOut}
            style={{
              backgroundColor: "transparent",
              color: "white",
              width: "5%",
            }}
          >
            Sign Out
          </button>
        </div>
      </nav>
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
                    {friend.showMovies ? "Hide Movies" : "Show Movies"}
                  </button>
                  {friend.showMovies && (
                    <div className="friend-dropdown">
                      {friend.movies.map((movie, movieIndex) => (
                        <a key={movieIndex}>
                          {movie.title}: {movie.score}/10 stars
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
          <button onClick={addFriend} className="btn btn-primary">
            Add Friend
          </button>
        </div>

        <button onClick={backToLandingPage} className="btn btn-primary">
          Return home
        </button>
      </div>
    </>
  );
};

export default ProfilePage;
