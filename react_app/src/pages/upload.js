import React from 'react';
import { Link } from 'react-router-dom';

const Upload = () => {
return (
	<div>
	<h1>This is where you can Upload and Update Packages on our Server</h1>
	<Link to='/upload-package'>Upload Package</Link>
	<br />
	<Link to='/update-package'>Update Package</Link>
	</div>
);
};

export default Upload;
