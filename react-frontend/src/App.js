import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LoginPage from './components/LoginPage';
import Wall from './components/Wall';
import React, {useState, useEffect} from 'react';
import ProfilePage from './components/Profile';
import Landing from './components/Landing';
import Baring from './components/Baring';


function App() {
  return (
      <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/wall" element={<Wall />} />
        <Route path='/profile' element={<ProfilePage />} />
        <Route path='/landing' element={<Landing />} />
        <Route path='/dashboard' element={<Baring />} />
      </Routes>
    </Router>
  );
}

export default App;
