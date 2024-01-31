import React, { useState } from 'react';

export default function ExpenseDelete(){
    const [expense, setExpense] =  useState('');

    const handleDeleteExpense = async() =>{
        fetch('http://localhost:5000/expense/' +  expense, {
            method: 'DELETE',
            headers: {
              'Content-Type': 'application/json',
            },
          })
          .then((response) => {
            if (!response.ok) 
              throw new Error(response.status);
              else return response.json();
          })
          .catch ((error) => {
            console.error('Error during deleting expense:', error);
          });
    };

    return (
        <div>
          <h2>Delete expense</h2>
          <label>Expense id:</label>
          <input type="text" value={expense} onChange={(e) => setExpense(e.target.value)} />

          <button onClick={handleDeleteExpense}>Delete expense</button>
          
        </div>
      );
}