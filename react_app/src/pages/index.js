import React, { useState } from 'react';
import axios from 'axios';

const Home = () => {

const [result, setResult] = useState(null);

const handleClick = () => {
	axios.get('http://localhost:8080/api/first')
	.then(response => {
		setResult(response.data.result);
	})
	.catch(error => {
		console.error(error);
	});
};

return (
	<div>
		<div><h1>Welcome to The Package Manager</h1>
		<h4>This website gives users the opportunity to browser a wide range of Node.js packages</h4>
		</div>
		<div>
		<em><p>Use the navigation bar at the top to choose different options for interacting with our package library. Ensure to Log In first. Only authenticated users can interact with our library.</p></em>
		</div>
		<button onClick={handleClick}>Click me</button>
    	{result && <p>Succesfully connected to Flask on port {result}</p>}
	</div>
);
};

export default Home;
