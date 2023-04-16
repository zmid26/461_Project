import React, { useState } from 'react';
import axios from 'axios';

const UpdatePackage = () => {
    const [id, setId] = useState('');

    const data = {
        "metadata": {
          "Name": "string",
          "Version": "1.2.3",
          "ID": "string"
        },
        "data": {
          "Content": "string",
          "URL": "string",
          "JSProgram": "string"
        }
      }
    const handleSubmit = (e) => {
        e.preventDefault();
        axios.put(`http://localhost:5000/package/${id}`, { data }, {
            headers: {
                'Content-Type': 'application/json',
                'X-Authorization': sessionStorage.getItem('token')
            }
            })
        .then(res => {
            console.log(res.data);
        })
        .catch(err => {
            console.log(err);
        })
    }
    return (
        <div>
            <h1>Use this to retrieve a package's rating</h1>
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
        </div>
    );
}

export default UpdatePackage;