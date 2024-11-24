// import React, { useState } from 'react';

// const DataTable = ({ column, table }) => {
//   return (
//     <table border="1">
//       <thead>
//         <tr>
//           {column.map((col, index) => (
//             <th key={index}>{col}</th>
//           ))}
//         </tr>
//       </thead>
//       <tbody>
//         {table.map((row, rowIndex) => (
//           <tr key={rowIndex}>
//             {row.map((cell, cellIndex) => (
//               <td key={cellIndex}>{cell}</td>
//             ))}
//           </tr>
//         ))}
//       </tbody>
//     </table>
//   );
// };


// function App() {
//   const [message, setMessage] = useState('加载中...');
  
//   const [sqlinput, setSqlInput] = useState('');  // 用户输入
//   const [data, setData] = useState({ 'column' : [], 'table' : [] })

//   // 加载初始数据
//   React.useEffect(() => {
//     console.log("backend url is")
//     console.log(process.env.REACT_APP_BACKEND_URL)
//     fetch(`${process.env.REACT_APP_BACKEND_URL}/api/hello`)
//       .then(response => response.json())
//       .then(data => setMessage(data.message))
//       .catch(error => console.error('错误:', error));
//   }, []);

//   // 处理表单提交
//   const handleSearchSubmit = (e) => {
//     e.preventDefault();
//     fetch(`${process.env.REACT_APP_BACKEND_URL}/api/search`, {
//       method: 'POST',
//       headers: {
//         'Content-Type': 'application/json'
//       },
//       body: JSON.stringify({ sqlinput })
//     })
//     .then(response => response.json())
//     .then(responseData => setData(responseData))
//     .catch(error => console.error('错误:', error));

//     console.log(typeof data.column)
//     console.log(data.column)
//     console.log(typeof data.table)
//     console.log(data.table)
//   };

//   const handleClear = () => {
//     setData({ 'column' : [], 'table' : [] })
//     setSqlInput('')
//   }

//   return (
//     <div>
//       <h1>DB Final Project Frontend / Backend Test</h1>
//       <p>{message}</p>

//       <form onSubmit={handleSearchSubmit}>
//         <input
//           type="text"
//           value={sqlinput}
//           onChange={(e) => setSqlInput(e.target.value)}
//           placeholder="輸入 sql 指令"
//         />
//         <button type="submit">Enter</button>
//       </form>

//       {/* {data.column && <p>query success</p>}  顯示後端回應 */}

//       {data.column && <DataTable column={data.column} table={data.table} />}

//       <button type="clear" onClick={handleClear}>clear</button>
//     </div>
//   );
// }

// export default App;



import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import ProtectedRoute from "./components/ProtectedRoute";
import AdminDashboard from "./pages/AdminDashboard";
import RestaurantDashboard from "./pages/RestaurantDashboard";
import CustomerDashboard from "./pages/CustomerDashboard";


function App() {
  // 初始化狀態時檢查 LocalStorage
  const [userType, setUserType] = useState(
    localStorage.getItem("userType") || null
  );
  const [username, setUsername] = useState(
    localStorage.getItem("username") || ""
  )


  // 處理登入
  const handleLogin = (type, name) => {
    setUserType(type);
    setUsername(name);
    localStorage.setItem("userType", type);
    localStorage.setItem("username", name);
  };

  // 處理登出
  const handleLogout = () => {
    setUserType(null)
    setUsername("")
    localStorage.removeItem("userType");
    localStorage.removeItem("username");
  };

  return (
    <Router>
      <Routes>
        {/* 登入頁面 */}
        <Route
          path="/login"
          element={
            userType ? (
              <Navigate to={`/${userType}Dashboard`} replace />
            ) : (
              <LoginPage onLogin={handleLogin} />
            )
          }
        />
        {/* 已登入頁面（受保護） */}
        <Route
          path="/CustomerDashboard"
          element={
            <ProtectedRoute userType={userType} allowedType="customer">
              <CustomerDashboard onLogout={handleLogout} /> {/* children of ProtectedRoute.js*/}
            </ProtectedRoute>
          }
        />
        <Route
          path="/RestaurantDashboard"
          element={
            <ProtectedRoute userType={userType} allowedType="restaurant">
              <RestaurantDashboard onLogout={handleLogout} />
            </ProtectedRoute>
          }
        />
        <Route
          path="/AdminDashboard"
          element={
            <ProtectedRoute userType={userType} allowedType="admin">
              <AdminDashboard onLogout={handleLogout} />
            </ProtectedRoute>
          }
        />
        {/* 根路徑預設導向 */}
        <Route path="*" element={<Navigate to={userType ? `/${userType}Dashboard` : "/login"} replace />} />
      </Routes>
    </Router>
  );
}

export default App;
