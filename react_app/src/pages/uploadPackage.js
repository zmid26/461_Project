import React, { useState } from 'react';
import axios from 'axios';

const UploadPackage = () => {
    const [file, setFile] = useState('');
    const [url, setUrl] = useState('');
    const [data, setData] = useState('');
    const [errormsg, setError] = useState('');
    const [errorcode, setCode] = useState('');
    const [errorbool, setErrorbool] = useState(false);

    const createBase64 = (e) => {
        const reader = new FileReader();
        reader.readAsDataURL(e);
        reader.onload = () => {
            setFile(reader.result);
        }
    }

    const handleSubmit = (e) => {
        e.preventDefault();
        const body = {
            content: file
        }
        axios.post(process.env.REACT_APP_SERVER_URL + ':' + process.env.REACT_APP_PORT_NUM + '/package', { body }, {
            headers: {
                'Content-Type': 'application/json',
                'X-Authorization': sessionStorage.getItem('token')
            }
            })
        .then(res => {
            console.log(res.data);
            setData(res.data);
        })
        .catch(error => {
            setError(error.message);
            setCode(error.code);
            setErrorbool(true);
        })
    };
    return (
        <div>
            <h1>Upload Packages</h1>
            <h3>Use either URL or Upload a zip file of package</h3>
            <div>
                <form onSubmit={handleSubmit}>
                <label>Enter Package URL: </label>
                <input
                type="text"
                placeholder="Search packages"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                />
                <br/>
                <label>Upload Package zip file: </label>
                <input
                type="file"
                accept=".zip"
                placeholder="Search packages"
                value={file}
                onChange={(e) => createBase64(e.target.value)}
                />
                <br/>
                <br/>
                <button type="submit">Upload</button>
                </form>
                </div>
                {errorbool && <div>
                <p>Error {errorcode}: {errormsg}</p>
                </div>}
                {data}
        </div>
    );
}

export default UploadPackage;
