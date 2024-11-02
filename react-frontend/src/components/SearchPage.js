import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import Autocomplete from 'react-autocomplete';

const SearchPage = () => {
  const [selectedMovies, setSelectedMovies] = useState([]);
  const [recentMovies, setRecentMovies] = useState([]);
  const [recommendedMovies, setRecommendedMovies] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const navigate = useNavigate();

  useEffect(() => {
    getRecentMovies();
    // window.location.href = 'https://disreputable-seance-wxrx9qjxv67hvjxv-3000.app.github.dev/search_page';
  }, []);

  const getRecentMovies = async () => {
    try {
      const response = await axios.get('/getRecentMovies');
      setRecentMovies(response.data.map(movie => movie.title));
    } catch (error) {
      console.error('Error fetching recent movies:', error);
    }
  };

  const handleSearch = async (e) => {
    const value = e.target.value;
    setSearchTerm(value);
    if (value.length >= 1) {
      try {
        const formData = new FormData();
        formData.append('q', value);
        const response = await axios.post('/search', formData);
        setSearchResults(response.data);
      } catch (error) {
        console.error('Search error:', error);
      }
    } else {
      setSearchResults([]);
    }
  };

  const handleSelect = (value) => {
    if (!selectedMovies.includes(value)) {
      setSelectedMovies([...selectedMovies, value]);
    }
    setSearchTerm('');
  };
  const handleRatingChange = (index, value) => {
    // Handle rating change logic here
    console.log(`Movie ${index} rated: ${value}`);
  };
  const handlePredict = async () => {
    if (selectedMovies.length === 0) {
      alert("Select at least 1 movie!!");
      return;
    }

    setIsLoading(true);
    setRecommendedMovies([]);

    try {
      const response = await axios.post('/predict', { movie_list: selectedMovies }, {
        headers: { 'Content-Type': 'application/json;charset=UTF-8' }
      });

      const { recommendations, imdb_id, web_url } = response.data;
      
      setRecommendedMovies(recommendations.map((title, index) => ({
        title,
        imdbId: imdb_id[index],
        webUrl: web_url[index]
      })));
    } catch (error) {
      console.error("Prediction error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSignOut = async () => {
    try {
      await axios.post('/out', { user: 'None' });
      navigate('/');
    } catch (error) {
      console.error('Sign out error:', error);
    }
  };

  return (
    <div>
      <nav style={{ backgroundColor: '#343a40', color: 'white', position: 'fixed', top: 0, left: 0, right: 0, zIndex: 1000 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', padding: '10px 20px' }}>
          <a href="#" style={{ color: 'white', textDecoration: 'none', fontSize: '1.25rem' }}>PopcornPicks🍿</a>
          <button onClick={handleSignOut} style={{ backgroundColor: 'transparent', color: 'white', border: 'none', cursor: 'pointer' }}>Sign Out</button>
        </div>
      </nav>

      <div style={{ marginTop: '60px', padding: '20px' }}>
        <div style={{ textAlign: 'center' }}>
          <h2 style={{ marginBottom: '5px' }}>🎬 Pick a Movie! 🎬</h2>
          <h6 style={{ marginBottom: '25px' }}>✨Tip: Select Up to 5 movies to get a tailored watchlist✨</h6>
        </div>

        <div style={{ display: 'flex', marginTop: '25px' }}>
          <div style={{ flex: '1', marginRight: '20px' }}>
            <h3>Selected Movie(s):</h3>
            <div style={{ display: 'flex', justifyContent: 'space-between' }}>
              <div style={{ width: '75%' }}>
                <Autocomplete
                  getItemValue={(item) => item}
                  items={searchResults}
                  renderItem={(item, isHighlighted) =>
                    <div key={item} style={{ backgroundColor: isHighlighted ? '#ddd' : '#fff' }}>{item}</div>
                  }
                  value={searchTerm}
                  onChange={handleSearch}
                  onSelect={handleSelect}
                  inputProps={{
                    style: { width: '100%', padding: '10px', borderRadius: '40px', border: '1px solid #ced4da', marginBottom: '20px' },
                    placeholder: "Search for a Movie"
                  }}
                />
                <ul style={{ listStyleType: 'none', paddingLeft: 0 }}>
                  {selectedMovies.map((movie, index) => (
                    <li key={index} style={{ padding: '10px', borderBottom: '1px solid #ced4da' }}>
                      {movie}
                      <button onClick={() => setSelectedMovies(selectedMovies.filter(m => m !== movie))} style={{
                        float: 'right',
                        backgroundColor: '#f8d7da',
                        borderRadius: '50%',
                        borderColor:'#f5c6cb',
                        cursor:'pointer'
                      }}>X</button>
                    </li>
                  ))}
                </ul>
              </div>
              <div style={{ width: '20%' }}>
                <button onClick={handlePredict} style={{
                  backgroundColor:'#007bff',
                  color:'white',
                  border:'none',
                  padding:'10px',
                  borderRadius:'5px',
                  cursor:'pointer'
                }}>Predict</button>
              </div>
            </div>
          </div>

          <div style={{ flex:'1' }}>
            <h3>Your Recents:</h3>
            <ul style={{ listStyleType:'none', paddingLeft:'0'}}>
              {recentMovies.map((movie,index)=>(
                <li key={index} style={{
                  padding:'10px',
                  borderBottom:'1px solid #ced4da'
                }}>{movie}</li>
              ))}
            </ul>
          </div>
        </div>

        <div style={{ marginTop: '60px' }}>
      <h2>Recommended Movies:</h2>
      <ul style={{ listStyleType: 'none', paddingLeft: '0' }}>
        {recommendedMovies.map((movie, index) => (
          <li key={index} style={{
            padding: '10px',
            borderBottom: '1px solid #ced4da'
          }}>
            {movie.title}
            {' '}
            (<a href={`https://www.imdb.com/title/${movie.imdbId}`} target="_blank" rel="noopener noreferrer">IMDb🔗</a>)
            {movie.webUrl && (
              <>
                {' '}
                (<a href={movie.webUrl} target="_blank" rel="noopener noreferrer">Stream Here!🍿</a>)
              </>
            )}
            <div className="rating-options">
              <label>
                <input
                  type="radio"
                  name={`rating-${index}`}
                  value="3"
                  onChange={() => handleRatingChange(index, 3)}
                />
                😍 Like
              </label>
              <label>
                <input
                  type="radio"
                  name={`rating-${index}`}
                  value="2"
                  onChange={() => handleRatingChange(index, 2)}
                />
                😐 Yet to Watch
              </label>
              <label>
                <input
                  type="radio"
                  name={`rating-${index}`}
                  value="1"
                  onChange={() => handleRatingChange(index, 1)}
                />
                😤 Dislike
              </label>
            </div>
          </li>
        ))}
      </ul>
    </div>

        {isLoading && (
          <div className="spinner-border" role="status" style={{
            position:'fixed',
            top:'50%',
            left:'50%',
            transform:'translate(-50%, -50%)'
          }}>
            <span className="sr-only">Loading...</span>
          </div>
        )}

        {/* Additional buttons or feedback sections can be added here */}
        
        {/* "Return home" button */}
        <button onClick={() => navigate('/')} className="btn btn-primary mx-auto" style={{
          display:'block',
          marginTop:'20px'
        }}>Return home</button>

      </div>
    </div>
  );
};

export default SearchPage;