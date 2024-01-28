import React, { useState, useEffect } from 'react';
import ExpenseAdd from '../add/ExpenseAdd';
import ShareAdd from '../add/ShareAdd';

function ExpenseList({user}) {
  const [expenses, setExpenses] = useState([]);
  const [addExpense, setAddExpense]  = useState(false);
  const [addShare, setAddShare]  = useState(false);
  
  const handleAddExpense =  async() =>  {
    setAddExpense(!addExpense);
  }
  
  const handleAddShare =  async() =>  {
    setAddShare(!addShare);
  }

  useEffect(() => {
    fetch('http://localhost:5000/expense')
      .then((response) => response.json())
      .then((data) => setExpenses(data));
  }, []);

  return (
    <div>
      <h2>Expense List</h2>
      <ul>
        {expenses.map((expense) => (
          <li key={expense.id}>{expense.id} - {expense.amount} zł, data wydatku: {expense.date}</li>
        ))}
      </ul>
      <button onClick={handleAddExpense}>Add expense</button>
      <button onClick={handleAddShare}>Add share</button>
      {addExpense  && <div>
        <ExpenseAdd user={user}/>
      </div>
      }
      {addShare  && <div>
        <ShareAdd/>
      </div>
      }
    </div>
  );
}

export default ExpenseList;