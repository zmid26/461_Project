import React, { useState } from 'react';
import { Link } from 'react-router-dom'

function LogIn() {
  const [username, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    // Here you can add code to submit the form to your backend
    console.log('Email:', username);
    console.log('Password:', password);
  };

  return (
    <div>
      <div>
        <h1>Sign In</h1>
        <form onSubmit={handleSubmit}>
          <div>
            <label>Username: </label>
            <input
              type="text"
              placeholder="Enter your username"
              value={username}
              onChange={(event) => setEmail(event.target.value)}
              required
            />
          </div>
          <br></br>
          <div>
            <label>Password:  </label>
            <input
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              required
            />
          </div>
          <button type="submit">Sign In</button>
        </form>
      </div>
      <div>
        <h2>Don't Have an Account?</h2>
        <Link to={"/newaccount"}>
          Create Account
        </Link>
      </div>
    </div>
  );
}

export default LogIn;
