import React, { useState } from 'react';
import axios from 'axios';

const DeletePackage = () => {
    const [id, setId] = useState('');
    const [name, setName] = useState('');

  const deletePackageId = async () => {
    await axios.delete(`http://localhost:8080/package/${id}`,{
      headers: {
        'Content-Type': 'application/json',
        'X-Authorization': sessionStorage.getItem('token')
      }
    })
      .then(response => {
        console.log(response);
      })
      .catch(error => {
        console.log(error);
      })
    };

  const deletePackageName = async () => {
    await axios.delete(`http://localhost:8080/package/${name}`,{
        headers: {
            'Content-Type': 'application/json',
            'X-Authorization': sessionStorage.getItem('token')
          }
        })
          .then(response => {
            console.log(response);
          })
          .catch(error => {
            console.log(error);
          });
  }

  return (
    <div>
        <h1>Delete Packages by ID or Name</h1>
    <div>
      <input
        type="text"
        placeholder="Enter package id"
        value={id}
        onChange={(e) => setId(e.target.value)}
      />
      <button onClick={deletePackageId}>Delete Package</button>
    </div>
    <br/>
    <p>OR</p>
    <br/>
    <div>
      <input
        type="text"
        placeholder="Enter package name"
        value={id}
        onChange={(e) => setName(e.target.value)}
      />
      <button onClick={deletePackageName}>Delete Package</button>
    </div>
    </div>
  );
}

export default DeletePackage;