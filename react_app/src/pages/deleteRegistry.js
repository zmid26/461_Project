import React, { useState } from 'react';
import axios from 'axios';

const DeleteRegistry = () => {
    const [isDeleted, setValue] = useState(false);

    const handleSubmit = (e) => {
        e.preventDefault();
        axios.delete(`http://localhost:8080/reset`)
            .then(res => {
                setValue(true);
                
                console.log(res.data);
            })
            .catch(err => {
                console.log(err);
            })
    }

    return (
        //create a button to delete the registry
        <div>
            <h1>Delete Registry</h1>
            <strong><h3>Make sure you want to delete this registry. Must be an admin to delete.
            <br /></h3></strong>
            <form>
                <input type="submit"  value="Delete Registry" onClick={handleSubmit}></input>
            </form>
            {isDeleted && <p>Registry Deleted</p>}
        </div>   
    )
}

export  default DeleteRegistry;