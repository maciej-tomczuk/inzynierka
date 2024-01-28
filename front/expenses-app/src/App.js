import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom"
import { Sidebar, Menu, MenuItem } from 'react-pro-sidebar';
import './App.css';
import './styles.css';
import UserList from './lists/UserList';
import ExpenseList from './lists/ExpenseList';
import ExpenseInGroupList from './lists/ExpenseInGroup';
import GroupList from './lists/GroupList';
import GroupMembersList from './lists/GroupMembersList';
import ShareList from './lists/ShareList';
import LoginForm from './LoginForm';
import RegisterForm from './RegisterForm';
import ShareAdd from './add/ShareAdd';
import ExpenseAdd from './add/ExpenseAdd';
import GroupAdd from './add/GroupAdd';
import MemberAdd from './add/MemberAdd';

function App() {
  const [user, setUserName] = useState([]);
  const [loggedInUser, setLoggedInUser] = useState(null);
  const [showRegister, setShowRegister] = useState(false);

  const handleLogin = (user) => {
    setUserName(user);
    setLoggedInUser(true);
  };
  const handleRegister = (user) => {
    setUserName(user);
    setLoggedInUser(true);
  };
  const switchToRegister = () => {
    setShowRegister(true);
  };
  const switchToLogin = () => {
    setShowRegister(false);
  };
  
  return (
    <div className="App">
      {!loggedInUser && !showRegister && <LoginForm onLogin={handleLogin} switchToRegister={switchToRegister} />}
      {!loggedInUser && showRegister && <RegisterForm onRegister={handleRegister} switchToLogin={switchToLogin} />} 
      {loggedInUser  &&
      <Router>
        
          <div id='div1'>
          <Sidebar label='Options' backgroundColor='#27db7d'>
            <Menu 
            menuItemStyles={{
              button: {
                [`&.active`]: {
                  backgroundColor: '#13395e',
                  color: '#b6c8d9',
                },
              },
            }}
            >
              <MenuItem component={<Link to="/users"/>}>Users</MenuItem>
              <MenuItem component={<Link to="/groups"/>}>Groups</MenuItem>
              <MenuItem component={<Link to="/members"/>}>Members</MenuItem>
              <MenuItem component={<Link to="/expenses"/>}>Expenses</MenuItem>
              <MenuItem component={<Link to="/groupexpenses"/>}>Expenses  in group</MenuItem>
              <MenuItem component={<Link to="/shares"/>}>Your shares</MenuItem>
            </Menu>
          </Sidebar>
          </div>
          <div id='div2'>
            <Routes>
              <Route  path="/users" element={<UserList/>}/>
              <Route  path="/shares" element={<ShareList user_id={user.id}/>}/>
              <Route  path="/expenses" element={<ExpenseList user={user}/>}/>
              <Route  path="/members" element={<GroupMembersList/>}/>
              <Route  path="/groups" element={<GroupList/>}/>
              <Route  path="/groupexpenses" element={<ExpenseInGroupList/>}/>
            </Routes>
          </div>
        
      </Router>
      
      }
    </div>
  );
}

export default App;