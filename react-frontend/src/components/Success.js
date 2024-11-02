import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const SuccessPage = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [emailSent, setEmailSent] = useState(false);
  const navigate = useNavigate();

  const handleNavigation = () => {
    navigate('/landing');
  };

  const styles = {
    container: {
      fontFamily: 'Arial, sans-serif',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      padding: '20px',
    },
    title: {
      fontSize: '24px',
      fontWeight: 'bold',
      marginBottom: '20px',
      color: 'white',
    },
    notifyDivs: {
      position: 'relative',
      width: '300px',
    },
    checkbox: {
      display: 'none',
    },
    formContainer: {
      overflow: 'hidden',
      transition: 'all 0.3s',
    },
    form: {
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
    },
    input: {
      width: '100%',
      padding: '10px',
      marginBottom: '10px',
      border: '1px solid #ccc',
      borderRadius: '4px',
    },
    button: {
      padding: '10px 20px',
      backgroundColor: '#007bff',
      color: 'white',
      border: 'none',
      borderRadius: '4px',
      cursor: 'pointer',
    },
    toggle: {
      display: 'inline-block',
      padding: '10px 20px',
      backgroundColor: '#f0f0f0',
      border: '1px solid #ccc',
      borderRadius: '4px',
      cursor: 'pointer',
    },
    orText: {
      margin: '20px 0',
      fontSize: '18px',
    },
    refreshButton: {
      padding: '10px 20px',
      backgroundColor: '#dc3545',
      color: 'white',
      border: 'none',
      borderRadius: '4px',
      cursor: 'pointer',
    },
    emailSentMessage: {
      position: 'absolute',
      top: '80px',
      left: '50%',
      transform: 'translateX(-50%)',
      backgroundColor: '#28a745',
      color: 'white',
      padding: '10px',
      borderRadius: '4px',
      display: emailSent ? 'block' : 'none',
    },
  };


  return (
    <div style={styles.container}>
      {isLoading && (
        <div style={{ display: 'flex', justifyContent: 'center' }}>
          <div className="spinner-border" role="status">
            <span className="sr-only"></span>
          </div>
        </div>
      )}
      <h1 style={styles.title}>We have successfully sent your watchlist to your registered email!</h1>
      <div style={styles.notifyDivs}>
        <div style={styles.formContainer}>
          <form style={styles.form}>
            <button style={styles.button} type="button" onClick={handleNavigation}>
              Return Home
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default SuccessPage;