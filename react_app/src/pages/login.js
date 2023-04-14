import React, { useState } from 'react';
import { Link } from 'react-router-dom';

function LogIn() {
  const [username, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [authed, setAuth] = useState(false);

  const handleSubmit = (event) => {
    const requestOptions = {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title: 'New Title', body: 'New body content' })
    };
    event.preventDefault();
    // Here you can add code to submit the form to your backend
    console.log('Email:', username);
    console.log('Password:', password);
    setAuth(true);
    fetch('https://localhost:8080', requestOptions)
      .then(response => response.json())
      .then(data => {
        setAuth(true)
      })
      .catch(error => {
        console.log(error);
        // Handle any errors
      });
  };

  return (
    <div>
      <h1>This is the Login Page</h1>
      {!authed &&
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
      </div>}
      {authed && <p>You Are now logged in!!</p>}
    </div>
  );
}

export default LogIn;
