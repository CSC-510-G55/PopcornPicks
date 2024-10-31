import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Wall from './components/Wall';
import React, {useState, useEffect} from 'react';


function App() {
  return (
      <Router>
      <Routes>
        <Route path="/wall" element={<Wall />} />
      </Routes>
    </Router>
  );
}

export default App;
