import React, { useState } from 'react';

export default function MemberDelete(){
    const [member, setMember] =  useState('');

    const handleDeleteMember = async() =>{
        fetch('http://localhost:5000/member/' +  member, {
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
            console.error('Error during deleting member:', error);
          });
    };

    return (
        <div>
          <h2>Delete member</h2>
          <label>Member id:</label>
          <input type="text" value={member} onChange={(e) => setMember(e.target.value)} />

          <button onClick={handleDeleteMember}>Delete Member</button>
          
        </div>
      );
}