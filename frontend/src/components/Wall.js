import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
const API_BASE_URL = process.env.REACT_APP_API_URL;

const Wall = () => {
	const [posts, setPosts] = useState([]);
	const [isLoading, setIsLoading] = useState(false);
	const navigate = useNavigate();

	useEffect(() => {
		loadPosts();
	}, []);

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
				// Navigate to the home page after a short delay
				setTimeout(() => {
					navigate('/');
				}, 1000);
			}
		} catch (error) {
			console.error('Sign out error:', error);
		}
	};

	const loadPosts = async () => {
		try {
			const response = await axios.get(`${API_BASE_URL}/getWallData`);
			setPosts(response.data);
		} catch (error) {
			console.error('Error loading posts:', error);
		}
	};

	const fetchMovieData = async (imdbID) => {
		try {
			const response = await axios.get('https://www.omdbapi.com/', {
				params: {
					i: imdbID,
					apikey: '77da67f1'
				}
			});

			return response.data;
		} catch (error) {
			console.error('Error fetching movie data:', error);
		}
	};

	const backToLandingPage = () => {
		navigate('/landing');
	};

	const renderStars = (score) => {
		const fullStars = Math.floor(score);
		const hasHalfStar = score % 1 > 0;

		return (
			<>
				{[...Array(fullStars)].map((_, i) => (
					<svg
						key={i}
						xmlns='http://www.w3.org/2000/svg'
						width='16'
						height='16'
						fill='currentColor'
						className='bi bi-star-fill'
						viewBox='0 0 16 16'
					>
						<path d='M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z' />
					</svg>
				))}
				{hasHalfStar && (
					<svg
						xmlns='http://www.w3.org/2000/svg'
						width='16'
						height='16'
						fill='currentColor'
						className='bi bi-star-half'
						viewBox='0 0 16 16'
					>
						<path d='M5.354 5.119 7.538.792A.516.516 0 0 1 8 .5c.183 0 .366.097.465.292l2.184 4.327 4.898.696A.537.537 0 0 1 16 6.32a.548.548 0 0 1-.17.445l-3.523 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256a.52.52 0 0 1-.146.05c-.342.06-.668-.254-.6-.642l.83-4.73L.173 6.765a.55.55 0 0 1-.172-.403.58.58 0 0 1 .085-.302.513.513 0 0 1 .37-.245l4.898-.696zM8 12.027a.5.5 0 0 1 .232.056l3.686 1.894-.694-3.957a.565.565 0 0 1 .162-.505l2.907-2.77-4.052-.576a.525.525 0 0 1-.393-.288L8.001 2.223 8 2.226v9.8z' />
					</svg>
				)}
			</>
		);
	};

	return (
		<div>
			<nav className='navbar navbar-expand-lg navbar-dark bg-dark topNavBar fixed-top'>
				<div className='container-fluid'>
					<a className='navbar-brand' href='#'>
						PopcornPicks🍿
					</a>
					<button
						type='button'
						id='signOut'
						onClick={handleSignOut}
						style={{
							backgroundColor: 'transparent',
							color: 'white',
							width: '5%'
						}}
					>
						Sign Out
					</button>
				</div>
			</nav>

			<div className='container' style={{ marginTop: '900px' }}>
				<div className='heading1'>
					<h2>
						<center>Popcorn Picks Wall</center>
					</h2>
					<p>
						<center>View other user ratings on movies!</center>
					</p>
					<button id='backToLanding' onClick={backToLandingPage} className='btn btn-primary mx-auto'>
						Return home
					</button>
				</div>
			</div>

			<div
				id='post-container'
				style={{
					margin: 'auto',
					maxWidth: '1000px',
					height: '95%',
					overflowY: 'auto'
				}}
			>
				{posts.map((post, index) => (
					<Post key={index} post={post} fetchMovieData={fetchMovieData} renderStars={renderStars} />
				))}
			</div>

			{isLoading && (
				<div id='loaderLanding' className='d-flex justify-content-center'>
					<div className='spinner-border' role='status'>
						<span className='sr-only'></span>
					</div>
				</div>
			)}
		</div>
	);
};

const Post = ({ post, fetchMovieData, renderStars }) => {
	const [movieData, setMovieData] = useState(null);

	useEffect(() => {
		const getMovieData = async () => {
			const data = await fetchMovieData(post.imdb_id);
			setMovieData(data);
		};

		getMovieData();
	}, [post.imdb_id, fetchMovieData]);

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
							<h5 className='card-title mb-0'>
								<span className='text-primary'>{post.username}</span> reviewed
							</h5>
							<small className='text-muted'>{movieData.Year}</small>
						</div>
						<h4 className='mb-3'>{movieData.Title}</h4>
						<div className='mb-2'>{renderStars(post.score)}</div>
						<p className='card-text'>{post.review}</p>
						<div className='mt-3'>
							<span className='badge bg-secondary me-2'>{movieData.Rated}</span>
							<span className='badge bg-info me-2'>{movieData.Genre}</span>
							<span className='badge bg-dark'>{movieData.Runtime}</span>
						</div>
					</div>
				</div>
			</div>
		</div>
	);
};

export default Wall;
