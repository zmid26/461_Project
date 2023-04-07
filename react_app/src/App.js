import React from 'react';
import './App.css';
import Navbar from './components/Navbar';
import { BrowserRouter as Router, Routes, Route}
	from 'react-router-dom';
import Home from './pages';
import Packages from './pages/packages';
import Rating from './pages/rating';
import LogIn from './pages/login';
import Upload from './pages/upload';
import NewAccount from './pages/newaccount';

function App() {
return (
	<Router>
	<Navbar />
	<Routes>
		<Route exact path='/' element={<Home />} />
		<Route path='/packages' element={<Packages/>} />
		<Route path='/upload' element={<Upload/>} />
		<Route path='/rating' element={<Rating/>} />
		<Route path='/login' element={<LogIn/>} />
    <Route path='/newaccount' element={<NewAccount/>} />
	</Routes>
	</Router>
);
}

export default App;
