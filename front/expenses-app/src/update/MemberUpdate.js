import React, { useState } from 'react';

export default function MemberUpdate(){
    const [role, setRole] =  useState('');
    const [member_id, setMemberId] =  useState('');

    const handleUpdateMember = async() =>{
        fetch('http://localhost:5000/member/' + member_id, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({role:role}),
          })
          .then((response) => {
            if (!response.ok) 
              throw new Error(response.status);
              else return response.json();
          })
          .catch ((error) => {
            console.error('Error during updating member:', error);
          });
    };

    return (
        <div>
          <h2>Update member</h2>
          <label>Membership id:</label>
          <input type="text" value={member_id} onChange={(e) => setMemberId(e.target.value)} />

          <label>Role in group:</label>
          <input type="text" value={role} onChange={(e) => setRole(e.target.value)} />
    
          <button onClick={handleUpdateMember}>Update member</button>
          
        </div>
      );
}