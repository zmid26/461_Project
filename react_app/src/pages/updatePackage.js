import React, { useState } from 'react';
import axios from 'axios';

const UpdatePackage = () => {
    const [id, setId] = useState('');
    const [errormsg, setError] = useState('');
    const [errorcode, setCode] = useState('');
    const [errorbool, setErrorbool] = useState(false);
    const [name, setName] = useState('');
    const [version, setVersion] = useState('');
    const [url, seturl] = useState('');
    let base64data = '';

    const createBase64 = (e) => {
        const reader = new FileReader();
        reader.readAsDataURL(e);
        reader.onload = () => {
            let res = reader.result;
            base64data = res.split(',')[1];
        }
        
    }
    
    const handleSubmit = (e) => {
        e.preventDefault();
        const data = {
        "metadata": {
          "Name": name,
          "Version": version,
          "ID": id
        },
        "data": {
                "content": base64data,
                "URL": url,
                "JSProgram": "if (process.argv.length === 7) {\nconsole.log('Success')\nprocess.exit(0)\n} else {\nconsole.log('Failed')\nprocess.exit(1)\n}\n"
        }
      };
        axios.put(process.env.REACT_APP_SERVER_URL + `/package/${id}`, { data }, {
            headers: {
                'Content-Type': 'application/json',
                'X-Authorization': sessionStorage.getItem('token')
            }
            })
        .then(res => {
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
            <h1>Use this to retrieve a package's rating</h1>
            <br></br>
            <form onSubmit={handleSubmit}>
                <label>Enter Package Name: </label>
                <input
                type="text"
                placeholder="package name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                />
                <br/>
                <label>Enter Package Version: </label>
                <input
                type="text"
                placeholder="package version"
                value={version}
                onChange={(e) => setVersion(e.target.value)}
                />
                <br/>
                <label>Enter Package ID: </label>
                <input
                type="text"
                placeholder="Search packages"
                value={id}
                onChange={(e) => setId(e.target.value)}
                />
                <br/>
                <label>Enter Package URL: </label>
                <input
                type="text"
                placeholder="package url"
                value={url}
                onChange={(e) => seturl(e.target.value)}
                />
                <br/>
                <br/>
                <label>Upload Package zip file: </label>
                <input
                type="file"
                accept=".zip"
                placeholder="Search packages"
                onChange={(e) => createBase64(e.target.files[0])}
                />
                <br/>
                <button type="submit">Search</button>
            </form>
            {errorbool && <div>
            <p>Error {errorcode}: {errormsg}</p>
            </div>}
        </div>
    );
}

export default UpdatePackage;