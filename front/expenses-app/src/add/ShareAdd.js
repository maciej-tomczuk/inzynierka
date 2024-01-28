import React, { useState } from 'react';

function ShareAdd(){
    const [expense, setExpense] =  useState('');
    const [user, setUser] =  useState('');
    const [share, setShare] =  useState('');

    const handleAddShare = async() =>{
        fetch('http://localhost:5000/share', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ expense_id:expense, user_id:user, share:share }),
          })
          .then((response) => {
            if (!response.ok) 
              throw new Error(response.status);
              else return response.json();
          })
          .catch ((error) => {
            console.error('Error during adding share:', error);
          });
    };

    return (
        <div>
          <h2>Add share</h2>
          <label>Expense id:</label>
          <input type="text" value={expense} onChange={(e) => setExpense(e.target.value)} />
    
          <label>User owing the money:</label>
          <input type="text" value={user} onChange={(e) => setUser(e.target.value)} />

          <label>Amount owed:</label>
          <input type="text" value={share} onChange={(e) => setShare(e.target.value)} />
    
          <button onClick={handleAddShare}>Add share</button>
          
        </div>
      );
}

export default ShareAdd;