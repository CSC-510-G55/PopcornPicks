import React, { useState } from 'react';
import axios from 'axios';
import Autocomplete from 'react-autocomplete';
import { useNavigate } from 'react-router-dom';

const API_BASE_URL = process.env.REACT_APP_API_URL;

const ReviewPage = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [selectedMovie, setSelectedMovie] = useState('');
  const [rating, setRating] = useState(0);
  const [comments, setComments] = useState('');
  const navigate = useNavigate();

  const handleSearch = async (value) => {
    setSearchTerm(value);
    if (value.length >= 1) {
      try {
        const formData = new FormData();
        formData.append('q', value);
        const response = await axios.post(`${API_BASE_URL}/search`, formData);
        setSearchResults(response.data);
      } catch (error) {
        console.error('Search error:', error);
      }
    } else {
      setSearchResults([]);
    }
  };

  const handleMovieSelect = (value) => {
    setSelectedMovie(value);
    setSearchTerm('');
  };
  const handleSignOut = async () => {
    const data = {
      user: 'None'
    };

    try {
      const response = await axios.post(`${API_BASE_URL}/out`, data, {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8'
        }
      });

      if (response.status === 200) {
        console.log('Signed out successfully');
        setTimeout(() => {
          navigate('/');
        }, 500);
      }
    } catch (error) {
      console.error('Sign out error:', error);
    }
  };
  const handleRatingChange = (value) => {
    setRating(value);
  };

  const submitReview = async () => {
    const data = {
      movie: selectedMovie,
      score: rating,
      review: comments,
    };

    try {
      await axios.post(`${API_BASE_URL}/review`, data);
      alert(`Review submitted for ${selectedMovie}. Rating: ${rating}/10`);
      setSelectedMovie('');
      setRating(0);
      setComments('');
    } catch (error) {
      alert('Error submitting review.');
      console.error('Submit review error:', error);
    }
  };

  const backToLandingPage = () => {
    // Implement navigation logic here
    navigate('/landing')
    console.log('Navigating back to landing page');
  };

  const styles = {
    body: {
        fontFamily: 'Arial, sans-serif',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '100vh',
        margin: 0,
        backgroundColor: 'rgba(255, 255, 255, 0.8)',
        color: 'black',
      },
      title: {
        fontSize: '48px',
        fontWeight: 'bold',
        color: 'black',
        margin: '20px 0',
      },
      container: {
        display: 'flex',
        width: '80%',
        backgroundColor: 'rgba(255, 255, 255, 0.9)',
        borderRadius: '10px',
        padding: '20px',
      },
      searchBar: {
        width: '50%',
        padding: '20px',
      },
      ratingSection: {
        width: '50%',
        padding: '20px',
        textAlign: 'left',
      },
      starContainer: {
        display: 'inline-block',
        fontSize: 0,
      },
      star: {
        display: 'inline-block',
        width: '30px',
        height: '30px',
        backgroundSize: 'cover',
        cursor: 'pointer',
      },
      comments: {
        width: '100%',
        boxSizing: 'border-box',
        marginTop: '10px',
      },
      submitBtn: {
        width: '100%',
        padding: '10px',
        marginTop: '10px',
        backgroundColor: '#4CAF50',
        color: 'white',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer',
      },
      backToLanding: {
        marginTop: '20px',
        padding: '10px 20px',
        backgroundColor: '#007bff',
        color: 'white',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer',
      },
  };

  return (
    <div style={styles.body}>
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark topNavBar fixed-top" id="landingTopNav">
        <div className="container-fluid">
          <a className="navbar-brand" href="/landing" >PopcornPicks🍿</a>
          <button 
            className="btn btn-outline-light"
            onClick={handleSignOut}
          >
            Sign Out
          </button>
          <button 
            className="navbar-toggler" 
            type="button" 
            data-bs-toggle="collapse" 
            data-bs-target="#navbarSupportedContent" 
            aria-controls="navbarSupportedContent" 
            aria-expanded="false" 
            aria-label="Toggle navigation"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
        </div>
      </nav>


      <div style={styles.title}>Review a Movie!</div>
      <div style={styles.container}>
        <div style={styles.searchBar}>
          <label htmlFor="movie-search">Search for a movie:</label>
          <Autocomplete
            getItemValue={(item) => item}
            items={searchResults}
            renderItem={(item, isHighlighted) =>
              <div style={{ background: isHighlighted ? 'lightgray' : 'white' }}>
                {item}
              </div>
            }
            value={searchTerm}
            onChange={(e) => handleSearch(e.target.value)}
            onSelect={handleMovieSelect}
          />
          {selectedMovie && (
            <ul style={{ listStyle: 'none', padding: 0 }}>
              <li style={{ padding: '10px', border: '1px solid #ced4da', borderRadius: '4px', marginTop: '10px' }}>{selectedMovie}</li>
            </ul>
          )}
        </div>
        <div style={styles.ratingSection}>
          <label htmlFor="movie-rating">Rate the movie:</label>
          <div style={styles.starContainer}>
            {[...Array(10)].map((_, index) => (
              <div
                key={index}
                style={{
                  ...styles.star,
                  backgroundImage: `url(${index < rating ? '/filledstar.png' : '/unfilledstar.png'})`,
                }}
                onClick={() => handleRatingChange(index + 1)}
              />
            ))}
          </div>
          <br />
          <br />
          <label htmlFor="comments">Comments:</label>
          <textarea
            id="comments"
            name="comments"
            rows="4"
            cols="50"
            style={styles.comments}
            value={comments}
            onChange={(e) => setComments(e.target.value)}
          />
          <button style={styles.submitBtn} onClick={submitReview}>Submit</button>
        </div>
      </div>
      <button style={styles.backToLanding} onClick={backToLandingPage}>
        Return home
      </button>
    </div>
  );
};

export default ReviewPage;