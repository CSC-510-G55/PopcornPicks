import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Wall from './components/Wall';
import React, {useState, useEffect} from 'react';
import ProfilePage from './components/Profile';
import Landing from './components/Landing';


function App() {
  return (
      <Router>
      <Routes>
        <Route path="/wall" element={<Wall />} />
        <Route path='/profile' element={<ProfilePage />} />
        <Route path='/landing' element={<Landing />} />
      </Routes>
    </Router>
  );
}

export default App;
