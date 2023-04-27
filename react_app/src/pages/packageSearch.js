import React, { useState } from 'react';
import axios from 'axios';

const PackageSearch = () => {
  const [id, setId] = useState('');
  const [search, setSearch] = useState(false);
  const [packagedata, setPackagedata] = useState([]);
  const [errormsg, setError] = useState('');
  const [errorcode, setCode] = useState('');
  const [errorbool, setErrorbool] = useState(false);

  const token = sessionStorage.getItem('auth_token');
  const handleSubmit = (event) => {
    event.preventDefault();
        axios.get(process.env.REACT_APP_SERVER_URL + `/package/${id}`, {
          headers: {
            'Content-Type': 'application/json',
            'X-Authorization': token
          }
        })
          .then(response => {
            setPackagedata(response.data);
            setSearch(true);
          })
          .catch(error => {
            setError(error.message);
            setCode(error.code);
            setErrorbool(true);
          });
    };

  return (
    <div>
      <h1>Use this to search for a Package by ID</h1>
      <br></br>
      <form onSubmit={handleSubmit}>
        <label>Enter Package ID: </label>
        <input
          type="text"
          placeholder="Search packages"
          value={id}
          onChange={(e) => setId(e.target.value)}
        />
        <button type="submit">Search</button>
      </form>
      <div>
        {search && 
        <div>
          <ul>
            <li>Metadata:</li>
            <ul>
              <li>Name: {packagedata.metadata.Name}</li>
              <li>Version: {packagedata.metadata.Version}</li>
              <li>ID: {packagedata.metadata.ID}</li>
            </ul>
            <li>Data:</li>
            <ul>
              <li>URL: {packagedata.data.URL}</li>
            </ul>
          </ul>
          </div>}
      </div>
      {errorbool && <div>
            <p>Error {errorcode}: {errormsg}</p>
            </div>}
    </div>
  );
}

export default PackageSearch;