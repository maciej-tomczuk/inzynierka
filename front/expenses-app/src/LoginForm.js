import React, { useState } from 'react';
import md5 from 'md5';

function LoginForm({ onLogin, switchToRegister }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async () => {
      const password_hashed = md5(password);
      console.log(password_hashed)

      fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username:username, password_hashed:password_hashed }),
      })
      .then((response) => {
        if (!response.ok){ 
          throw new Error(response.status);
        }
          else return response.json();
      })
      .then((data) =>{
        onLogin(data);
      })
      .catch ((error) => {
        console.error('Error during login:', error);
      });
    };

  return (
    <div>
      <h2>Login</h2>
      <label>Username:</label>
      <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />

      <label>Password:</label>
      <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />

      <button onClick={handleLogin}>Login</button>
      
      <p>
        Don't have an account?{' '}
        <span style={{ cursor: 'pointer', color: 'blue' }} onClick={switchToRegister}>
          Register
        </span>
      </p>
    </div>
  );
}

export default LoginForm;