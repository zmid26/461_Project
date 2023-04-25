import React, { useState } from 'react';
import axios from 'axios';


const NameSearch = () => {
    const [regex, setRegex] = useState("");
    const [result, setResult] = useState("");
    const [errormsg, setError] = useState('');
    const [errorcode, setCode] = useState('');
    const [errorbool, setErrorbool] = useState(false);

    const eventHandler = (e) => {
        e.preventDefault();
        axios.post(process.env.REACT_APP_SERVER_URL + ':' + process.env.REACT_APP_PORT_NUM + '/package/byRegex',{ regex }, {
            headers: {
                'Content-Type': 'application/json',
                'X-Authorization': sessionStorage.getItem('token')
            }
        })
        .then(response => {
            setResult(response.data);
        })
        .catch(error => {
            setError(error.message);
            setCode(error.code);
            setErrorbool(true);
        });
    }
    return (
        <div>
            <h1>Search for Packages by Using Regular Expressions</h1>
            <h3>Enter a regular expression below</h3>
            <div>
                <form onSubmit={eventHandler}>
                    <label>Enter a regex: </label>
                    <input type="text"
                    value={regex}
                    onChange={(e) => setRegex(e.target.value)}/>
                    <button type="submit">Search</button>
                </form>
            </div>
            {errorbool && <div>
            <p>Error {errorcode}: {errormsg}</p>
            </div>}
        {result}
        </div>
    )
}

export default NameSearch;