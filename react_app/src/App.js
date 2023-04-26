import React from 'react';
import './App.css';
import Navbar from './components/Navbar';
import { BrowserRouter as Router, Routes, Route}
	from 'react-router-dom';
import Home from './pages';
import Packages from './pages/packages';
import LogIn from './pages/login';
import Upload from './pages/upload';
import NewAccount from './pages/newaccount';
import GetHistory from './pages/packageHistory';
import DeleteRegistry from './pages/deleteRegistry';
import PackageSearch from './pages/packageSearch';
import DeletePackage from './pages/packageDelete';
import RatePackage from './pages/ratePackage';
import UploadPackage from './pages/uploadPackage';
import UpdatePackage from './pages/updatePackage';
import NameSearch from './pages/nameSearch';
import TestPage from './pages/testPage';

// import {
// 	BrowserRouter as Router,
// 	Routes,
// 	Route,
// }

function App() {
return (
	<Router>
	<Navbar />
	<Routes>
		<Route exact path='/' element={<Home />} />
		<Route path='/packages' element={<Packages/>} />
		<Route path='/upload' element={<Upload/>} />
		<Route path='/login' element={<LogIn/>} />
    	<Route path='/newaccount' element={<NewAccount/>} />
		<Route path='/package-history' element={<GetHistory/>} />
		<Route path='/delete' element={<DeleteRegistry/>} />
		<Route path='/package-search' element={<PackageSearch/>} />
		<Route path='/package-delete' element={<DeletePackage/>} />
		<Route path='/rating' element={<RatePackage/>} />
		<Route path='/upload-package' element={<UploadPackage/>} />
		<Route path='/update-package' element={<UpdatePackage/>} />
		<Route path='/package-search-by-name' element={<NameSearch/>} />
		<Route path='/test' element={<TestPage/>} />

	</Routes>
	</Router>
);
}

export default App;
