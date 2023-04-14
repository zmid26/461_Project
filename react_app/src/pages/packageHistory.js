import React, {useState} from "react";

function GetHistory() {
    const [packageName, setPackage] = useState('');

    const handleSubmit = (event) => {
        event.preventDefault();
        // Here you can add code to submit the form to your backend
        console.log('Package:', packageName);
    };
    return(
        <div>
            <h1>Here, you can retrieve the history of package by searching for it by name</h1>
            <h3>Enter Name of Package Below</h3>
            <form onSubmit={handleSubmit}>
                <div>
                <label>Package Name: </label>
                <input
                type="text"
                placeholder="Package Name"
                value={packageName}
                onChange={(event) => setPackage(event.target.value)}
                required
                />
                </div>
                <button type="submit">Submit</button>
            </form>
        </div>
    );
}

export default GetHistory;