import React, { useState } from 'react';

function NewAccount() {
  const [username, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confpassword, setConfirm] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    // Here you can add code to submit the form to your backend
    if(password === confpassword) {
        console.log('Email:', username);
        console.log('Password:', password);
    }
    else {
        console.log("passwords do not match");
    }
  };

  return (
    <div>
      <div>
        <h1>Create a New Account:</h1>
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
          <br></br>
          <div>
            <label>Confirm Password: </label>
            <input 
              type="password"
              placeholder="Confirm your password"
              value={confpassword}
              onChange={(event) => setConfirm(event.target.value)}
              required
              />
          </div>
          <button type="submit">Sign In</button>
        </form>
      </div>
    </div>
  );
}

export default NewAccount;
