import React, { useState } from 'react';
import md5 from 'md5';

export default function UserUpdate({user_id}) {
  const [name, setName] = useState('');
  const [password, setPassword] = useState('');

  const handleUpdateUser  = async() => {
    const password_hashed = md5(password);
    fetch('http://localhost:5000/user/' + user_id, {
        method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ password_hashed:password_hashed, name:name}),
    })
      .then((response) => response.json())
  }

  return (
    <div>
      <h2>Update your data</h2>
      <label>Name:</label>
      <input type="text" value={name} onChange={(e) => setName(e.target.value)} />

      <label>Password:</label>
      <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />

      <button onClick={handleUpdateUser}>Update</button>
    </div>
  );
}