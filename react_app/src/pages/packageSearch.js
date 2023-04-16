import React, { useState } from 'react';
import axios from 'axios';

const PackageSearch = () => {
  const [id, setId] = useState('');
  const [search, setSearch] = useState(false);
  const [packagedata, setPackagedata] = useState([]);
  const token = sessionStorage.getItem('auth_token');
  const handleSubmit = (event) => {
    event.preventDefault();
        axios.put(`https://localhost:8080/package/${id}`, {
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
            console.log(error);
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
        {search && <ul>
        {packagedata.map(post => (
          <li key={post.id}>{post.title}</li>
        ))}
      </ul>}
      </div>
    </div>
  );
}

export default PackageSearch;