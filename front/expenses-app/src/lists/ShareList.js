import React, { useState, useEffect } from 'react';

function ShareList({user_id}) {
  const [shares, setShares] = useState([]);

  useEffect(() => {
    const url = 'http://localhost:5000/share/u/' + user_id;
    fetch(url)
      .then((response) => response.json())
      .then((data) => setShares(data));
  }, []);

  return (
    <div>
      <h2>Shares List</h2>
      <ul>
        {shares.map((share) => (
          <li key={share.id}>{share.id} - {share.share}</li>
        ))}
      </ul>
    </div>
  );
}

export default ShareList;