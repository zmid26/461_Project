import React, { useState } from 'react';
import axios from 'axios';
import PackageList from '../components/packageList';


const NameSearch = () => {
    const [regex, setRegex] = useState("");
    const [result, setResult] = useState("");
    const [valid, setValid] = useState(false);
    const [errormsg, setError] = useState('');
    const [errorcode, setCode] = useState('');
    const [errorbool, setErrorbool] = useState(false);

    const eventHandler = (e) => {
        e.preventDefault();
        axios.post(process.env.REACT_APP_SERVER_URL + '/package/byRegex',{ regex }, {
            headers: {
                'Content-Type': 'application/json',
                'X-Authorization': sessionStorage.getItem('token')
            }
        })
        .then(response => {
            setResult(response.data);
            setValid(true);
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
        {valid && <PackageList packages={result}/>}
        </div>
    )
}

export default NameSearch;