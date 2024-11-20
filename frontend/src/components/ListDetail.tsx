import React, { useEffect,useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

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
    const [movies, setMovies] = useState<Movie[]|null>(null);

    useEffect(() => {
        const fetchList = async () => {
            try {
                const response = await axios.get(`${API_BASE_URL}/lists/${slug}`);
                if (response.status === 200) {
                    setMovies(response.data.movies);
                }
                
            } catch (error) {
                console.error("List fetch error:", error);
            }
        };

        fetchList();
    }, [slug]);

    if (!movies) {
        return <p>Loading...</p>;
    }

    return (
        <div className="text-white">
            <h1>List: {slug}</h1>
            <ul>
                {movies.map((movie) => (
                    <li key={movie.movieId}>
                        <a href={`https://www.imdb.com/title/${movie.imdb_id}`} target="_blank" rel="noreferrer">
                            {movie.title}
                        </a>
                    </li>
                ))}
            </ul>
        </div>
    );
}