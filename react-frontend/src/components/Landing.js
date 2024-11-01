import React from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import '../LandingPage.css'; // You'll need to create this CSS file

const Landing = () => {
  const navigate = useNavigate();

  const handleSignOut = async () => {
    const data = {
      user: 'None'
    };

    try {
      const response = await axios.post('/out', data, {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8'
        }
      });

      if (response.status === 200) {
        console.log('Signed out successfully');
        // Navigate to the home page after a short delay
        setTimeout(() => {
          navigate('/');
        }, 1000);
      }
    } catch (error) {
      console.error('Sign out error:', error);
    }
  };

  const handleNavigation = (path) => {
    navigate(path);
  };

  return (
    <div className="landing-page">
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark topNavBar fixed-top" id="landingTopNav">
        <div className="container-fluid">
          <a className="navbar-brand" href="#">PopcornPicks🍿</a>
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

      <div className="container" id="centralDivLanding">
        <div className="heading1">
          <h2 className="text-center">🎬 PopcornPicks🍿: Pick a Movie! 🎬</h2>
          <p className="text-center text-light">
            Discover personalized movie recommendations by selecting up to 5 of your favorite films.
            <br /> 
            Create a watchlist and have it conveniently sent to your email.
            <br />
            Enjoy movies at your own pace, on your terms.
          </p>
          <div className="d-flex justify-content-center flex-wrap">
            <button 
              className="btn btn-primary m-2"
              onClick={() => handleNavigation('/search_page')}
            >
              Get Started!
            </button>
            <button 
              className="btn btn-primary m-2"
              onClick={() => handleNavigation('/wall')}
            >
              Go to Wall!
            </button>
            <button 
              className="btn btn-primary m-2"
              onClick={() => handleNavigation('/review')}
            >
              Review a Movie!
            </button>
            <button 
              className="btn btn-primary m-2"
              onClick={() => handleNavigation('/profile')}
            >
              Profile
            </button>
          </div>
          <div className="highlighted-section text-center">
            <p>Made with ❤️ by <a href="https://github.com/Shrimadh/PopcornPicks" target="_blank" rel="noopener noreferrer">PopcornPicks</a></p>     
            <a href="https://github.com/Shrimadh/PopcornPicks/blob/master/LICENSE.md" target="_blank" rel="noopener noreferrer">MIT License Copyright (c) 2024 PopcornPicks</a>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Landing;