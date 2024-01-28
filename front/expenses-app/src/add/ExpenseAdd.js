import React, { useState } from 'react';

export default function ExpenseAdd({user}){
    const [group, setGroup] =  useState('');
    const [amount, setAmount] =  useState('');
    const [description, setDesc] =  useState('');

    const handleAddExpense = async() =>{
        fetch('http://localhost:5000/expense', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_id:user.id, group_id:group, amount:amount, description:description }),
          })
          .then((response) => {
            if (!response.ok) 
              throw new Error(response.status);
              else return response.json();
          })
          .catch ((error) => {
            console.error('Error during adding expense:', error);
          });
    };

    return (
        <div>
          <h2>Add expense</h2>
          <label>Group id:</label>
          <input type="text" value={group} onChange={(e) => setGroup(e.target.value)} />

          <label>Amount:</label>
          <input type="text" value={amount} onChange={(e) => setAmount(e.target.value)} />

          <label>Description:</label>
          <input type="text" value={description} onChange={(e) => setDesc(e.target.value)} />
          <button onClick={handleAddExpense}>Add expense</button>
          
        </div>
      );
}