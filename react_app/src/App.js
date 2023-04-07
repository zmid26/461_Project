import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [result, setResult] = useState(null);

  const handleClick = () => {
    axios.get('http://localhost:8080/api/first')
      .then(response => {
        setResult(response.data.result);
      })
      .catch(error => {
        console.error(error);
      });
  };

  return (
    <div>
        <button onClick={handleClick}>Click me</button>
        {result && <p>The result is {result}</p>}
    </div>
  );
}

export default App