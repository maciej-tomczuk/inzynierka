import React, { useState } from 'react';
import MemberAdd from '../add/MemberAdd';
import MemberDelete from '../delete/MemberDelete';
import MemberUpdate from '../update/MemberUpdate';

function GroupMembersList() {
  const [members, setMembers] = useState([]);
  const [group, setGroup] = useState('')
  const [addMember, setAddMember]  = useState(false);
  const [deleteMember, setDeleteMember]  = useState(false);
  const [updateMember, setUpdateMember]  = useState(false);
  
  const handleMembers =  async() =>{
    fetch('http://localhost:5000/member/'  + group)
      .then((response) => response.json())
      .then((data) => setMembers(data));
  };

  const handleAddMember =  async() =>  {
    setAddMember(!addMember);
  }
  const handleDeleteMember =  async() =>  {
    setDeleteMember(!deleteMember);
  }
  const handleUpdateMember =  async() =>  {
    setUpdateMember(!updateMember);
  }

  return (
    <div>
      <h2>Member List</h2>
      <label>Choose group:</label>
      <input type="text" value={group} onChange={(e) => setGroup(e.target.value)} />
      <button onClick={handleMembers}>Show</button>      
      <ul>
        {members.map((member) => (
          <li key={member.id}>Membership ID: {member.id},  User ID: {member.user_id}, role: {member.role}</li>
        ))}
        
      </ul>
      <button onClick={handleAddMember}>Add member</button>
      <button onClick={handleDeleteMember}>Delete member</button>
      <button onClick={handleUpdateMember}>Update member</button>

      {addMember  && <div>
        <MemberAdd/>
      </div>
      }
      {deleteMember  && <div>
        <MemberDelete/>
      </div>
      }
      {updateMember  && <div>
        <MemberUpdate/>
      </div>
      }
    </div>
  );
}

export default GroupMembersList;