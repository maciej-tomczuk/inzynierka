import React, { useState } from 'react';

export default function GroupUpdate(){
    const [name, setName] =  useState('');
    const [description, setDesc] =  useState('');
    const [group_id, setGroupId] =  useState('');

    const handleUpdateGroup = async() =>{
        fetch('http://localhost:5000/group/' + group_id, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ group_name:name, description:description}),
          })
          .then((response) => {
            if (!response.ok) 
              throw new Error(response.status);
              else return response.json();
          })
          .catch ((error) => {
            console.error('Error during updating group:', error);
          });
    };

    return (
        <div>
          <h2>Update group</h2>

          <label>ID:</label>
          <input type="text" value={group_id} onChange={(e) => setGroupId(e.target.value)} />

          <label>Name:</label>
          <input type="text" value={name} onChange={(e) => setName(e.target.value)} />
    
          <label>Description:</label>
          <input type="text" value={description} onChange={(e) => setDesc(e.target.value)} />
    
          <button onClick={handleUpdateGroup}>Update group</button>
          
        </div>
      );
}