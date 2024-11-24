import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL;

const fetchMovieData = async (imdbID) => {
	try {
		const response = await axios.get(`${API_BASE_URL}/movies/${imdbID}`);

		return response.data;
	} catch (error) {
		console.error('Error fetching movie data:', error);
	}
};

const Movie = ({ imdbID }) => {
	const [movieData, setMovieData] = useState(null);

	useEffect(() => {
		const getMovieData = async () => {
			const data = await fetchMovieData(imdbID);
			setMovieData(data);
		};

		getMovieData();
	}, [imdbID]);

	if (!movieData) return null;

	return (
		<div className='card mb-4 shadow-sm'>
			<div className='row g-0'>
				<div className='col-md-3 col-lg-2'>
					<img
						src={movieData.Poster}
						alt={movieData.Title}
						className='img-fluid rounded-start'
						style={{ maxHeight: '200px', objectFit: 'cover' }}
					/>
				</div>
				<div className='col-md-9 col-lg-10'>
					<div className='card-body'>
						<div className='d-flex justify-content-between align-items-center mb-2'>
							<h4 className='mb-3'>{movieData.Title}</h4>
							<small className='text-muted'>{movieData.Year}</small>
						</div>
						<div className='mt-3'>
							<span className='badge bg-secondary me-2'>{movieData.Rated}</span>
							<span className='badge bg-info me-2'>{movieData.Genre}</span>
							<span className='badge bg-dark'>{movieData.Runtime}</span>
						</div>
						<div className='mt-3'>
							<a href={`https://www.imdb.com/title/${imdbID}`} target='_blank' rel='noopener noreferrer'>
								<img src='/imdb.png' alt='IMDb' style={{ width: '50px' }} />
							</a>
						</div>
					</div>
				</div>
			</div>
		</div>
	);
};

export default Movie;
