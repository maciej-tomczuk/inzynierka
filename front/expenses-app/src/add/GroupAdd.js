import React, { useState } from 'react';

function GroupAdd(){
    const [name, setName] =  useState('');
    const [description, setDesc] =  useState('');

    const handleAddGroup = async() =>{
        fetch('http://localhost:5000/group', {
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
            console.error('Error during adding group:', error);
          });
    };

    return (
        <div>
          <h2>Add group</h2>
          <label>Name:</label>
          <input type="text" value={name} onChange={(e) => setName(e.target.value)} />
    
          <label>Description:</label>
          <input type="text" value={description} onChange={(e) => setDesc(e.target.value)} />
    
          <button onClick={handleAddGroup}>Add group</button>
          
        </div>
      );
}

export default GroupAdd;