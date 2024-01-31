import React, { useState, useEffect } from 'react';
import GroupAdd from '../add/GroupAdd';
import GroupDelete from '../delete/GroupDelete';
import GroupUpdate from '../update/GroupUpdate';

export default function GroupList() {
  const [groups, setGroups] = useState([]);
  const [addGroup, setAddGroup]  = useState(false);
  const [deleteGroup, setDeleteGroup]  = useState(false);
  const [updateGroup, setUpdateGroup]  = useState(false);

  const handleAddGroup =  async() =>  {
    setAddGroup(!addGroup);
  }
  const handleDeleteGroup =  async() =>  {
    setDeleteGroup(!deleteGroup);
  }
  const handleUpdateGroup =  async() =>  {
    setUpdateGroup(!updateGroup);
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
          <li key={group.id}>Group ID:{group.id}, group name: {group.group_name}, decsription: {group.description}</li>
        ))}
      </ul>
      <button onClick={handleAddGroup}>Add group</button>
      <button onClick={handleUpdateGroup}>Update group</button>
      <button onClick={handleDeleteGroup}>Delete group</button>
      
      {addGroup  && <div>
        <GroupAdd/>
      </div>
      }
      {deleteGroup  && <div>
        <GroupDelete/>
      </div>
      }
      {updateGroup  && <div>
        <GroupUpdate/>
      </div>
      }
    </>
  );
}