import React, { useState, useEffect } from 'react';
import GroupAdd from '../add/GroupAdd';
import MemberAdd from '../add/MemberAdd';

export default function GroupList() {
  const [groups, setGroups] = useState([]);
  const [addGroup, setAddGroup]  = useState(false);
  const [addMember, setAddMember]  = useState(false);

  const handleAddGroup =  async() =>  {
    setAddGroup(!addGroup);
  }

  const handleAddMember =  async() =>  {
    setAddMember(!addMember);
  }

  useEffect(() => {
    fetch('http://localhost:5000/group')
      .then((response) => response.json())
      .then((data) => setGroups(data));
  }, []);

  return (
    <>
      <h2>Group List</h2>
      <ul>
        {groups.map((group) => (
          <li key={group.id}>{group.group_name}</li>
        ))}
      </ul>
      <button onClick={handleAddGroup}>Add group</button>
      <button onClick={handleAddMember}>Add member</button>
      {addGroup  && <div>
        <GroupAdd/>
      </div>
      }
      {addMember  && <div>
        <MemberAdd/>
      </div>
      }
    </>
  );
}