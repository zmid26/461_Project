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
import GetHistory from './pages/packageHistory';
import DeleteRegistry from './pages/deleteRegistry';
import PackageSearch from './pages/packageSearch';

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
		<Route path='/packages/history' element={<GetHistory/>} />
		<Route path='/delete' element={<DeleteRegistry/>} />
		<Route path='/packages/search' element={<PackageSearch/>} />'
	</Routes>
	</Router>
);
}

export default App;
