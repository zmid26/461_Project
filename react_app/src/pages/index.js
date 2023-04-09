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
	<h1>Welcome to The Packages Manager</h1>
	<button onClick={handleClick}>Click me</button>
    {result && <p>Succesfully connected to Flask on port {result}</p>}
	</div>
);
};

export default Home;
