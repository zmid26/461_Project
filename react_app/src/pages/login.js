import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

function LogIn() {
  const [username, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [authed, setAuth] = useState(false);

  const handleSubmit = (event) => {
    event.preventDefault();
    // Here you can add code to submit the form to your backend
    const data = {
      "User": {
        "name": {username},
        "isAdmin": true
      },
      "Secret": {
        "password": {password}
      }
    }
    

    useEffect(() => {
    axios.put('https://localhost:8080/authenticate', { data }, {
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(response => {
        sessionStorage("auth_token",response.data);
        setAuth(true);
      })
      .catch(error => {
        console.log(error);
      });
    }, []);
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
      {authed && <div>
        <p>You Are now logged in!!</p>
        <p> Authentication Token: {sessionStorage.getItem("auth_token")}</p>
      </div>}
    </div>
  );
}

export default LogIn;
