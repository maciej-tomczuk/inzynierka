import React, { useState, useEffect } from 'react';

function GroupMembersList() {
  const [members, setMembers] = useState([]);
  const [group, setGroup] = useState('')
  
  const handleMembers =  async() =>{
    fetch('http://localhost:5000/member/'  + group)
      .then((response) => response.json())
      .then((data) => setMembers(data));
  };

  return (
    <div>
      <h2>Member List</h2>
      <label>Choose group:</label>
      <input type="text" value={group} onChange={(e) => setGroup(e.target.value)} />
      <button onClick={handleMembers}>Show</button>      
      <ul>
        {members.map((member) => (
          <li key={member.id}>{member.user_id} - {member.role}</li>
        ))}
      </ul>
    </div>
  );
}

export default GroupMembersList;