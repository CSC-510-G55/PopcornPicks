import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LoginPage from './components/LoginPage';
import Wall from './components/Wall';
import React, {useState, useEffect} from 'react';
import ProfilePage from './components/Profile';
import Landing from './components/Landing';
import SearchPage from './components/SearchPage';


function App() {
  return (
      <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/wall" element={<Wall />} />
        <Route path='/profile' element={<ProfilePage />} />
        <Route path='/landing' element={<Landing />} />
        <Route path='/search_page' element={<SearchPage />} />
      </Routes>
    </Router>
  );
}

export default App;
