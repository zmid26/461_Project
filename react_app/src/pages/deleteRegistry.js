import React, { useState } from 'react';
import axios from 'axios';

const DeleteRegistry = () => {
    const [isDeleted, setValue] = useState(false);
    const [errormsg, setError] = useState('');
    const [errorcode, setCode] = useState('');
    const [errorbool, setErrorbool] = useState(false);

    const handleSubmit = (e) => {
        e.preventDefault();
        axios.delete(process.env.REACT_APP_SERVER_URL + ':' + process.env.REACT_APP_PORT_NUM + '/reset')
            .then(res => {
                setValue(true);
                
                console.log(res.data);
            })
            .catch(error => {
                setError(error.message);
                setCode(error.code);
                setErrorbool(true);
            })
    }

    return (
        <div>
        <div>
            <h1>Delete Registry</h1>
            <strong><h3>Make sure you want to delete this registry. Must be an admin to delete.
            <br /></h3></strong>
            <form>
                <input type="submit"  value="Delete Registry" onClick={handleSubmit}></input>
            </form>
            {isDeleted && <p>Registry Deleted</p>}
        </div>   
        {errorbool && <div>
            <p>Error {errorcode}: {errormsg}</p>
            </div>}
        </div>
    )
}

export  default DeleteRegistry;