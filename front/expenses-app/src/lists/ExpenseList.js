import React, { useState, useEffect } from 'react';
import ExpenseAdd from '../add/ExpenseAdd';
import ShareAdd from '../add/ShareAdd';
import ExpenseDelete from '../delete/ExpenseDelete';
import ExpenseUpdate from '../update/ExpenseUpdate';

function ExpenseList({user}) {
  const [expenses, setExpenses] = useState([]);
  const [addExpense, setAddExpense]  = useState(false);
  const [addShare, setAddShare]  = useState(false);
  const [deleteExpense, setDeleteExpense]  = useState(false);
  const [updateExpense, setUpdateExpense]  = useState(false);
  
  const handleAddExpense =  async() =>  {
    setAddExpense(!addExpense);
  }
  
  const handleUpdateExpense =  async() =>  {
    setUpdateExpense(!updateExpense);
  }
  const handleAddShare =  async() =>  {
    setAddShare(!addShare);
  }

  const handleDeleteExpense  =  async() =>  {
    setDeleteExpense(!deleteExpense);
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
          <li key={expense.id}>Expense ID: {expense.id}, amount: {expense.amount} zł, description: {expense.description}, owner: {expense.user_id} date: {expense.date}</li>
        ))}
      </ul>
      <button onClick={handleAddExpense}>Add expense</button>
      <button onClick={handleAddShare}>Add share</button>
      <button onClick={handleDeleteExpense}>Delete expense</button>
      <button onClick={handleUpdateExpense}>Update expense</button>

      {addExpense  && <div>
        <ExpenseAdd user={user}/>
      </div>
      }
      {addShare  && <div>
        <ShareAdd/>
      </div>
      }
      {deleteExpense  && <div>
        <ExpenseDelete/>
      </div>
      }
      {updateExpense  && <div>
        <ExpenseUpdate/>
      </div>
      }
    </div>
  );
}

export default ExpenseList;