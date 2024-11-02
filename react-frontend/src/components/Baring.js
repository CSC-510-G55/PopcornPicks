import React, { useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2';
import axios from 'axios';
import { Chart as ChartJS, CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend } from 'chart.js';
import { useNavigate } from 'react-router-dom';
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);


//const genreData = { Action: 10, Adventure: 30, Drama: 40, Romance: 22, Crime: 31 };
const Baring = () => {
    const [genreData, setGenreData] = useState({});
    const navigate = useNavigate();
    // State for chart data
    const [chartData, setChartData] = useState({ labels: [], datasets: [] });

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
              navigate('/');
          }
        } catch (error) {
          console.error('Sign out error:', error);
        }
      };
    // Function to generate random colors
    const getRandomColor = () => {
        const r = Math.floor(Math.random() * 255);
        const g = Math.floor(Math.random() * 255);
        const b = Math.floor(Math.random() * 255);
        return `rgba(${r}, ${g}, ${b}, 0.7)`;
    };
    const handleNavigation = (path) => {
        navigate(path);
      };
    // Fetch genre data from the backend
    useEffect(() => {
        fetch('/getGenreCount')
            .then(response => response.json())
            .then(data => setGenreData(data))
            .catch(error => console.error('Error fetching genre data:', error));
    }, []);

    useEffect(() => {
        console.log("genres");
        // Extract genre names and values from genreData
        const labels = Object.keys(genreData);
        const dataValues = Object.values(genreData);

        // Generate random colors based on the number of genres
        const backgroundColor = labels.map(() => getRandomColor());
        const borderColor = backgroundColor.map(color => color.replace('0.7', '1')); // Solid color for borders

        // Update chart data
        setChartData({
            labels,
            datasets: [
                {
                    label: 'Genre Popularity',
                    data: dataValues,
                    backgroundColor,
                    borderColor,
                    borderWidth: 2,
                    hoverBackgroundColor: 'rgba(0, 0, 0, 0.1)',
                },
            ],
        });
    }, [genreData]);

    const options = {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: false,
                text: 'Movie Genre Popularity',
            },
        },
        animations: {
            tension: {
                duration: 1000,
                easing: 'easeInBounce',
                from: 0.5,
                to: 0,
                loop: false,
            },
            y: {
                easing: 'easeOutBounce',
                duration: 1500,
            },
        },
    };

    // Inline styling
    const containerStyle = {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        height: '100vh',
        fontFamily: 'Arial, sans-serif',
    };

    const chartContainerStyle = {
        width: '70%',
        backgroundColor: '#fff',
        padding: '20px',
        boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
        borderRadius: '8px',
    };

    const titleStyle = {
        textAlign: 'center',
        color: 'white',
        marginBottom: '20px',
    };

    return (
        <><nav className="navbar navbar-expand-lg navbar-dark bg-dark topNavBar fixed-top" id="landingTopNav">
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
        <div style={containerStyle}>
            <h1 style={titleStyle}>Movie Genre Popularity Chart!</h1>
            <div style={chartContainerStyle}>
                <Bar data={chartData} options={options} />
            </div>
            <button 
              className="btn btn-primary m-2"
              onClick={() => handleNavigation('/landing')}
            >Return Home</button>
        </div>
        </>
    );
};

export default Baring;
