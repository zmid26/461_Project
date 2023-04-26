import React from 'react';

function PackageList(props) {
  const pkgs = props.data;

  return (
    <div>
      <h2>Package List</h2>
      <ul>
        {pkgs.map(pkg => (
          <div>
          <li>Name: {pkg.Name}</li>
          <li>Version: {pkg.Version}</li>
          <br/>
          </div>
        ))}
      </ul>
    </div>
  );
}

export default PackageList;