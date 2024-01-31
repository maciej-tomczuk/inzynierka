import React, { useState } from 'react';

export default function ShareDelete(){
    const [share, setShare] =  useState('');

    const handleDeleteShare = async() =>{
        fetch('http://localhost:5000/share/' +  share, {
            method: 'DELETE',
            headers: {
              'Content-Type': 'application/json',
            },
          })
          .then((response) => {
            if (!response.ok) 
              throw new Error(response.status);
              else return response.json();
          })
          .catch ((error) => {
            console.error('Error during deleting share:', error);
          });
    };

    return (
        <div>
          <h2>Delete share</h2>
          <label>Share id:</label>
          <input type="text" value={share} onChange={(e) => setShare(e.target.value)} />

          <button onClick={handleDeleteShare}>Delete share</button>
          
        </div>
      );
}