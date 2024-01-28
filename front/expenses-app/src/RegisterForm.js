import React, { useState } from 'react';
import md5 from 'md5';

function RegisterForm({ onRegister, switchToLogin }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');

  const handleRegister = async () => {
      const password_hashed = md5(password);
      console.log(password_hashed)

      fetch('http://localhost:5000/user', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({ username:username, password_hashed:password_hashed, name:name }),
      })
      .then((response) => {
        if (!response.ok) 
          throw new Error(response.status);
          else return response.json();
      })
      .then ((data) => {
        onRegister(data);
      })
      .catch ((error) => {
        console.error('Error during registration:', error);
      });
    };

  return (
    <div>
      <h2>Register</h2>
      <label>Username:</label>
      <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />

      <label>Full name:</label>
      <input type="text" value={name} onChange={(e) => setName(e.target.value)} />

      <label>Password:</label>
      <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />

      <button onClick={handleRegister}>Register</button>

      <p>
        Already have an account?{' '}
        <span style={{ cursor: 'pointer', color: 'blue' }} onClick={switchToLogin}>
          Login
        </span>
      </p>
    </div>
  );
}

export default RegisterForm;