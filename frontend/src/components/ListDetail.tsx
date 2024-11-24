import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import Movie from './Movie';

const API_BASE_URL = process.env.REACT_APP_API_URL;

export interface Movie {
	movieId: number;
	genres: string;
	imdb_id: string;
	name: string;
	title: string;
	overview: string;
	poster_path: string;
	runtime: number;
}

export default function ListDetail() {
	const { slug } = useParams();
	const [title, setTitle] = useState<string>('');
	const [movies, setMovies] = useState<Movie[] | null>(null);

	useEffect(() => {
		const fetchList = async () => {
			try {
				const response = await axios.get(`${API_BASE_URL}/lists/${slug}`);
				if (response.status === 200) {
					setMovies(response.data.movies);
					setTitle(response.data.name);
				}
			} catch (error) {
				console.error('List fetch error:', error);
			}
		};

		fetchList();
	}, [slug]);

	if (!movies) {
		return <p>Loading...</p>;
	}

	return (
		<div className='text-white'>
			<h1 style={{ marginTop: '50px', marginBottom: '32px' }}>List: {title || slug}</h1>
			<div style={{ maxHeight: 'calc(80vh)', overflow: 'scroll' }}>
				{movies.map((movie) => (
					<Movie key={movie.movieId} imdbID={movie.imdb_id} />
				))}
			</div>
		</div>
	);
}
