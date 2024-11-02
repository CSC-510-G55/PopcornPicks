import React, { useEffect } from 'react';

const SearchPageRedirect = () => {
  useEffect(() => {
    window.location.href = 'http://localhost:5000/search_page';
  }, []);

  return <div>Redirecting to search page...</div>;
};

export default SearchPageRedirect;