import React, { useState } from 'react';

function MemberAdd(){
    const [group, setGroup] =  useState('');
    const [user, setUser] =  useState('');
    const [role, setRole] =  useState('');

    const handleAddMember = async() =>{
        fetch('http://localhost:5000/member', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ group_id:group, user_id:user, role:role}),
          })
          .then((response) => {
            if (!response.ok) 
              throw new Error(response.status);
              else return response.json();
          })
          .catch ((error) => {
            console.error('Error during adding member:', error);
          });
    };

    return (
        <div>
          <h2>Add member</h2>
          <label>User id:</label>
          <input type="text" value={user} onChange={(e) => setUser(e.target.value)} />
    
          <label>Group id:</label>
          <input type="text" value={group} onChange={(e) => setGroup(e.target.value)} />

          <label>Role in group:</label>
          <input type="text" value={role} onChange={(e) => setRole(e.target.value)} />
    
          <button onClick={handleAddMember}>Add member</button>
          
        </div>
      );
}

export default MemberAdd;