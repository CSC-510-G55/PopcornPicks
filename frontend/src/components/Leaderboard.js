import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import '../Leaderboard.css';

const API_BASE_URL = process.env.REACT_APP_API_URL;

const Leaderboard = () => {
	const navigate = useNavigate();
	const [leaderboard, setLeaderboard] = useState([]);

	useEffect(() => {
		const fetchLeaderboard = async () => {
			try {
				const response = await axios.get(`${API_BASE_URL}/leaderboard`);
				setLeaderboard(response.data);
			} catch (error) {
				console.error('Leaderboard fetch error:', error);
			}
		};
		fetchLeaderboard();
	}, []);

	return (
		<div className='leaderboard-page'>
			<div className='leaderboard-container bg-dark text-center'>
				<h1 className='leader px-5 py-5 text-white'>Leaderboard</h1>
				<div className='px-5'>
					{leaderboard.length > 0 ? (
						<table className='table table-striped text-white'>
							<thead>
								<tr>
									<th>#</th>
									<th>Username</th>
									<th>Score</th>
								</tr>
							</thead>
							<tbody>
								{leaderboard.map((entry, index) => (
									<tr key={index}>
										<td>{index + 1}</td>
										<td>{entry.username}</td>
										<td>{entry.score}</td>
									</tr>
								))}
							</tbody>
						</table>
					) : (
						<p className='text-white'>No leaderboard entries available.</p>
					)}
				</div>
				<button className='btn btn-primary my-5' onClick={() => navigate('/landing')}>
					Back to Landing Page
				</button>
			</div>
		</div>
	);
};

export default Leaderboard;
