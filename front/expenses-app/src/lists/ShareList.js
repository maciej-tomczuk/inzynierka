import React, { useState, useEffect } from 'react';
import ShareDelete from '../delete/ShareDelete';

function ShareList({user_id}) {
  const [shares, setShares] = useState([]);
  const [deleteShare, setDeleteShare] =  useState('');

  useEffect(() => {
    const url = 'http://localhost:5000/share/u/' + user_id;
    fetch(url)
      .then((response) => response.json())
      .then((data) => setShares(data));
  }, []);

  const handleDeleteShare =  async() =>  {
    setDeleteShare(!deleteShare);
  }

  return (
    <div>
      <h2>Shares List</h2>
      <ul>
        {shares.map((share) => (
          <li key={share.id}>{share.id} - {share.share}</li>
        ))}
      </ul>
      <button onClick={handleDeleteShare}>Delete share</button>
      {deleteShare  &&  <div>
      <ShareDelete/>
    </div>}
    </div>
  );
}

export default ShareList;