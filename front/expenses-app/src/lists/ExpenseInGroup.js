import React, { useState, useEffect } from 'react';

function ExpenseInGroupList() {
  const [expenses, setExpenses] = useState([]);
  const [group, setGroup] = useState('');

  const handleExpenses = async() => {
    fetch('http://localhost:5000/expense/g/' + group)
      .then((response) => response.json())
      .then((data) => setExpenses(data));
  };

  return (
    <div>
      <h2>Expense List</h2>
      <label>Choose group:</label>
      <input type="text" value={group} onChange={(e) => setGroup(e.target.value)} />
      <button onClick={handleExpenses}>Show</button>  
      <ul>
        {expenses.map((expense) => (
          <li key={expense.id}>Expense ID: {expense.id}, amount: {expense.amount} zł, description: {expense.description}, owner: {expense.user_id} date: {expense.date}</li>
        ))}
      </ul>
    </div>
  );
}

export default ExpenseInGroupList;