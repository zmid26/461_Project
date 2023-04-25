import React, { useState } from 'react';
import axios from 'axios';

const RatePackage = () => {
    const [id, setId] = useState('');
    const [rating, setRating] = useState('');
    const [israted, setRated] = useState(false);
    const [errormsg, setError] = useState('');
    const [errorcode, setCode] = useState('');
    const [errorbool, setErrorbool] = useState(false);

    const handleSubmit = (e) => {
        e.preventDefault();
        axios.get(process.env.REACT_APP_SERVER_URL + ':' + process.env.REACT_APP_PORT_NUM + `/${id}/rate`, {
            headers: {
                'Content-Type': 'application/json',
                'X-Authorization': sessionStorage.getItem('token')
            }
            })
            .then(response => {
                setRating(response.data);
                setRated(true);
            })
            .catch(error => {
                setError(error.message);
                setCode(error.code);
                setErrorbool(true);
            }
            );
        }
    return (
        <div>
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
            {israted && <div>
                <p>Rating:{rating.map(post => (
          <li key={post.id}>{post.title}</li>
        ))}</p>
            </div>}
            {errorbool && <div>
            <p>Error {errorcode}: {errormsg}</p>
            </div>}
        </div>
    );
}

export default RatePackage;