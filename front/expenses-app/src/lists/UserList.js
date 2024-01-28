import React, { useState, useEffect } from 'react';

function UserList() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    // Fetch users
    fetch('http://localhost:5000/user')
      .then((response) => response.json())
      .then((data) => setUsers(data));
  }, []);

  return (
    <div>
      <h2>User List</h2>
      <ul>
        {users.map((user) => (
          <li key={user.id}>Id: {user.id}, Name: {user.name}</li>
        ))}
      </ul>
    </div>
  );
}

export default UserList;