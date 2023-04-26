import React from 'react';

function HistoryList(props) {
  const pkg = props.data;

  return (
    <div>
      <h2>Package List</h2>
      <ul>
        {pkg.map(version => (
          <div>
          <li>User:</li>
          <ul>
            <li>name: {version.User.name}</li>
            <li>Admin: {version.User.Admin}</li>
          </ul>
          <li>Date: {version.Date}</li>
          <li>Metadata:</li>
          <ul>
            <li>package name: {version.Metadata.Name}</li>
            <li>package version: {version.Metadata.Version}</li>
            <li>package ID: {version.Metadata.ID}</li>
          </ul>
          <br/>
          <br/>
          </div>
        ))}
      </ul>
    </div>
  );
}

export default HistoryList;