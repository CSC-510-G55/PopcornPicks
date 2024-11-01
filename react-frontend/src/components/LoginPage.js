import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import '../LoginPage.css'; // You'll need to create this CSS file for styling
// import '../stylesheet.css';

const LoginPage = () => {
  const [isCreatingAccount, setIsCreatingAccount] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [newUsername, setNewUsername] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [dupPassword, setDupPassword] = useState('');
  const [showLoginError, setShowLoginError] = useState(false);
  const [showMismatchError, setShowMismatchError] = useState(false);
  const [showInvalidUsernameError, setShowInvalidUsernameError] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const login = async () => {
    // Implement login logic here
    setIsLoading(true);
    setShowLoginError(false);
    try {
      const response = await axios.post('/log', {
        username,
        password
      }, {
        headers: {
          'Content-Type': 'application/json;charset=UTF-8'
        }
      });

      if (response.status === 200) {
        // Successful login
        setTimeout(() => {
          navigate('/landing');
        }, 2000);
      }
    } catch (error) {
      setShowLoginError(true);
      setUsername('');
      setPassword('');
    } finally {
      setIsLoading(false);
    }
  };

  const createAccount = () => {
    setIsCreatingAccount(true);
  };

  const makeAccount = async () => {
    if (newPassword !== dupPassword) {
      setShowMismatchError(true);
      return;
    }
    setShowMismatchError(false);
    setShowInvalidUsernameError(false);
    
    try {
      const response = await axios.post('/', {
        username: newUsername,
        password: newPassword,
        email
      });

      if (response.status === 200) {
        // Account created successfully
        setIsCreatingAccount(false);
        // Optionally, you can automatically log in the user here
      }
    } catch (error) {
      if (error.response && error.response.status === 400) {
        setShowInvalidUsernameError(true);
      }
    }
  };


  const continueAsGuest = () => {
    // Implement guest login logic here
    navigate('/landing'); // Assuming guest users are redirected to the landing page
  };

  return (
    <div className='login-page'>
      <nav class="navbar navbar-expand-lg navbar-dark bg-dark topNavBar fixed-top" id="loginTopNav">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">PopcornPicks🍿</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
    </div>
  </nav>
  
    <div className="container" style={{ marginTop: '60px' }} id="centralDivLogin">
      {!isCreatingAccount ? (
        <div className="heading1">
          <h1 style={{ marginBottom: '5px' }}>
            <center>🎬 PopcornPicks🍿: Log In</center>
          </h1>
          <div className="wrapper">
            <center>
              <input
                className="form-control mr-sm-2"
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                style={{ width: '30%', borderRadius: '40px', marginBottom: '20px' }}
              />
              <input
                className="form-control mr-sm-2"
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                style={{ width: '30%', borderRadius: '40px' }}
              />
            </center>
            {showLoginError && (
              <div id="logInError">
                <h3 style={{ color: 'red' }}>Incorrect Username or Password</h3>
              </div>
            )}
          </div>
          <center>
            <div style={{ width: '35%', height: '20%' }}>
              <button onClick={login} className="btn btn-primary mx-auto">Login</button>
              <button onClick={createAccount} className="btn btn-primary mx-auto">Create an Account</button>
            </div>
          </center>
          <br />
          <button onClick={continueAsGuest} className="btn btn-primary mx-auto">Continue as Guest</button>
          <br /><br />
          <div className="highlighted-section">
            <p>Made with ❤️ by <a href="https://github.com/Shrimadh/PopcornPicks" target="_blank" rel="noopener noreferrer">PopcornPicks</a></p>
            <a href="https://github.com/Shrimadh/PopcornPicks/blob/master/LICENSE.md" target="_blank" rel="noopener noreferrer">MIT License Copyright (c) 2024 PopcornPicks</a>
          </div>
        </div>
      ) : (
        <div id="createAccountForm">
          <div className="container" style={{ width: '100%', display: 'block' }}>
            <h1>
              <center>🎬 PopcornPicks🍿: Create an Account</center>
            </h1><br /><br />
            <center>
              <h3>Enter Your Email:</h3>
              <input
                className="form-control mr-sm-2"
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                style={{ width: '50%', borderRadius: '40px' }}
              />
              <h3>Create Your Username:</h3>
              <input
                className="form-control mr-sm-2"
                type="text"
                placeholder="Username"
                value={newUsername}
                onChange={(e) => setNewUsername(e.target.value)}
                style={{ width: '50%', borderRadius: '40px' }}
              />
              <h3>Create Your Password:</h3>
              <input
                className="form-control mr-sm-2"
                type="password"
                placeholder="Password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                style={{ width: '50%', borderRadius: '40px' }}
              />
              <h3>Re-enter Your Password:</h3>
              <input
                className="form-control mr-sm-2"
                type="password"
                placeholder="Re-enter Password"
                value={dupPassword}
                onChange={(e) => setDupPassword(e.target.value)}
                style={{ width: '50%', borderRadius: '40px' }}
              />
            </center>
            {showMismatchError && (
              <div id="misMatchPass">
                <h3 style={{ color: 'red' }}>Passwords do not match!</h3>
              </div>
            )}
            {showInvalidUsernameError && (
              <div id="invalidUsername">
                <h3 style={{ color: 'red' }}>Invalid Username</h3>
              </div>
            )}
            <br />
            <div>
              <center>
                <button onClick={makeAccount} className="btn btn-primary mx-auto">Create Account</button>
              </center>
            </div>
          </div>
        </div>
      )}
      {isLoading && (
        <div id="loaderLogin">
          <center>
            <h3>Logging In:</h3>
          </center>
          <div className="spinner-border" role="status">
            <span className="sr-only"></span>
          </div>
        </div>
      )}
    </div>
    </div>
  );
};

export default LoginPage;