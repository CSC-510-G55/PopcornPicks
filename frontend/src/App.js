import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LoginPage from './components/LoginPage';
import Wall from './components/Wall';
import ProfilePage from './components/Profile';
import Landing from './components/Landing';
import Baring from './components/Baring';
import SearchPage from './components/SearchPage';
import ReviewPage from './components/Reviews';
import SuccessPage from './components/Success';
import Lists from './components/Lists.tsx';
import ListDetail from './components/ListDetail.tsx';
import Quiz from './components/Quiz.js';
import Leaderboard from './components/Leaderboard.js';
import Seasonal from './components/Seasonal';

function App() {
	return (
		<Router>
			<Routes>
				<Route path='/' element={<LoginPage />} />
				<Route path='/wall' element={<Wall />} />
				<Route path='/profile' element={<ProfilePage />} />
				<Route path='/landing' element={<Landing />} />
				<Route path='/dashboard' element={<Baring />} />
				<Route path='/lists' element={<Lists />} />
				<Route path='/lists/:slug' element={<ListDetail />} />
				<Route path='/seasonal' element={<Seasonal />} />
				<Route path='/search_page' element={<SearchPage />} />
				<Route path='/reviews' element={<ReviewPage />} />
				<Route path='/success' element={<SuccessPage />} />
				<Route path='/quiz' element={<Quiz />} />
				<Route path='/leaderboard' element={<Leaderboard />} />
			</Routes>
		</Router>
	);
}

export default App;
