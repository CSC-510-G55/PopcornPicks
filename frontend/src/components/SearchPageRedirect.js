import React, { useEffect } from 'react';

const API_BASE_URL = process.env.REACT_APP_API_URL;

const SearchPageRedirect = () => {
	useEffect(() => {
		window.location.href = 'http://localhost:5001/search_page';
	}, []);

	return <div>Redirecting to search page...</div>;
};

export default SearchPageRedirect;
