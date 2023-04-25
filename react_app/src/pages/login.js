import React, { useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

const LogIn = () => { 
  const [username, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [authed, setAuth] = useState(false);
  const [errormsg, setError] = useState('');
  const [errorcode, setCode] = useState('');
  const [errorbool, setErrorbool] = useState(false);

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
    

    axios.put(process.env.REACT_APP_SERVER_URL + '/authenticate', { data }, {
      headers: {
        'Content-Type': 'application/json'
      }
    })
      .then(response => {
        sessionStorage("auth_token",response.data);
        console.log(response.data);
        setAuth(true);
      })
      .catch(error => {
        setError(error.message);
        setCode(error.code);
        setErrorbool(true);
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
      {errorbool && <div>
        <p>Error {errorcode}: {errormsg}</p>
        </div>}
      {authed && <div>
        <p>You Are now logged in!!</p>
        <p> Authentication Token: {sessionStorage.getItem("auth_token")}</p>
      </div>}
    </div>
  );
}

export default LogIn;
