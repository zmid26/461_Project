import React from "react";
import { Link } from 'react-router-dom';

const About = () => {
return (
	<div>
	<h1>
		Here, you can browse through, and interact with the packages we have!
	</h1>
	<div>
		<Link to="/package-history">
			Retrieve a packages history
		</Link>
		<br></br>
		<Link to="/package-delete">
			Delete a package
		</Link>
		<br></br>
		<Link to="/package-search">
			Search for a package
		</Link>
		<br></br>
		<Link to="/package-search-by-name">
			Search for a package by name
		</Link>
	</div>
	</div>
);
};

export default About;
