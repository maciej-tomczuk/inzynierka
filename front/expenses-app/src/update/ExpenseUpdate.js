import React, { useState } from 'react';

export default function ExpenseUpdate(){
    const [amount, setAmount] =  useState('');
    const [description, setDesc] =  useState('');
    const [expense_id, setExpenseId] =  useState('');

    const handleUpdateExpense = async() =>{
        fetch('http://localhost:5000/expense/' + expense_id, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ amount:amount, description:description}),
          })
          .then((response) => {
            if (!response.ok) 
              throw new Error(response.status);
              else return response.json();
          })
          .catch ((error) => {
            console.error('Error during updating expense:', error);
          });
    };

    return (
        <div>
          <h2>Update expense</h2>

          <label>ID:</label>
          <input type="text" value={expense_id} onChange={(e) => setExpenseId(e.target.value)} />

          <label>Amount:</label>
          <input type="text" value={amount} onChange={(e) => setAmount(e.target.value)} />
    
          <label>Description:</label>
          <input type="text" value={description} onChange={(e) => setDesc(e.target.value)} />
    
          <button onClick={handleUpdateExpense}>Update expense</button>
          
        </div>
      );
}