import React, { useState } from 'react';

export default function GroupDelete(){
    const [group, setGroup] =  useState('');
    const [data, setData] = useState([]);

    const handleDeleteGroup = async() =>{
        fetch('http://localhost:5000/group/' +  group, {
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
            console.error('Error during deleting group:', error);
          });

          fetch('http://localhost:5000/expense/g/' +  group, {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json',
            },
          })
          .then((response) => {
            if (!response.ok) 
              throw new Error(response.status);
              else return response.json();
          })
          .then((data) => {
            setData(data);
          })
          .catch ((error) => {
            console.error('Error during deleting group:', error);
          });

          handleDeleteGroupExpenses();
        }

        const handleDeleteGroupExpenses = async() =>{
          data.map((data) => (
            fetch('http://localhost:5000/expense/' +  data.id, {
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
            })
          ));
        
        }
    

    return (
        <div>
          <h2>Delete group</h2>
          <label>Group id:</label>
          <input type="text" value={group} onChange={(e) => setGroup(e.target.value)} />
          <button onClick={handleDeleteGroup}>Delete group</button>
        </div>
      );
}