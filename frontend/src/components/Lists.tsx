import React, { useState } from 'react';
import Autocomplete from 'react-autocomplete';
import axios from 'axios';
import './List.css'
import { useNavigate } from 'react-router-dom';

const API_BASE_URL = process.env.REACT_APP_API_URL;

const Lists = () => {
  const navigate = useNavigate();
  const [movies, setMovies] = useState<string[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [searchResults, setSearchResults] = useState<string[]>([]);

  const handleSearch = async (value: string) => {
    setSearchTerm(value);
    if (value.length >= 1) {
      try {
        const formData = new FormData();
        formData.append("q", value);
        const response = await axios.post(`${API_BASE_URL}/search`, formData);
        setSearchResults(response.data.filter((name: string) => !movies.includes(name)));
      } catch (error) {
        console.error("Search error:", error);
      }
    } else {
      setSearchResults([]);
    }
  };

  const handleSelect = (value: string) => {
    setMovies([...movies, value]);
    setSearchTerm("");
    setSearchResults([]);
  };

  const handleRemoveMovie = (movie: string) => {
    setMovies(movies.filter(m => m !== movie));
  };

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    
    const name = prompt("Enter list name:");

    if (!name) return;

    const data = {
      name,
      movies
    };

    axios.post(`${API_BASE_URL}/lists`, data)
      .then((res) => {
        setMovies([]);
        navigate(`/lists/${res.data.slug}`);
      })
      .catch((error) => {
        console.error("List creation error:", error)
      });
  };

  return (
    <div className="container">
      <div className="mt-3">
        <h2 className='text-white'>Add Movies</h2>
        <ul className="list-group">
          {movies.map((movie, index) => (
            <li key={index} className="list-group-item d-flex justify-content-between align-items-center">
              {movie}
              <button className="btn btn-danger btn-sm" onClick={() => handleRemoveMovie(movie)}>Remove</button>
            </li>
          ))}
        </ul>
        <Autocomplete
            getItemValue={(item: string) => item}
            items={searchResults}
            renderItem={(item: string, isHighlighted: boolean) => (
              <div
                style={{ background: isHighlighted ? "lightgray" : "white" }}
              >
                {item}
              </div>
            )}
            value={searchTerm}
            onChange={(e) => handleSearch(e.target.value)}
            onSelect={handleSelect}
          />
          <button type="submit" onClick={handleSubmit} className="btn btn-primary text-white">Submit</button>
      </div>
    </div>
  );
};

export default Lists;