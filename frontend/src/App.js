// App.js 整個網頁的主程式

// 引入套件、跟其它 .js 寫的函式，這裡跟後端使用其它檔案實作的函式的概念很像
// 比較重要的差別是，這些 .js 檔函式的回傳值通常是網頁元素的 Component，可以想成是螢幕該有的畫面的一部分
import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import LoginPage from "./pages/LoginPage"; // 一開始看到的登入畫面
import ProtectedRoute from "./components/ProtectedRoute"; // 路由檢查，防一些不預期的事情（上網查）
import AdminDashboard from "./pages/AdminDashboard"; // admin 的已登入畫面
import RestaurantDashboard from "./pages/RestaurantDashboard"; // restaurant 的已登入畫面
import CustomerDashboard from "./pages/CustomerDashboard"; // customer 的已登入畫面


function App() {
  // 初始化一個「狀態變數」，初始值為全域變數 "userType" 的值
  // 可以上網暸解 useState 狀態變數的功用
  const [userType, setUserType] = useState(
    localStorage.getItem("userType") || null
  );

  // 處理登入的函式，會當成參數傳給 pages/LoginPage.js，當身份驗證成功時會被呼叫
  const handleLogin = (type, name) => {
    // 參數為使用者的類別（Customer, restaurant, admin）跟名字
    setUserType(type);
    localStorage.setItem("userType", type);
    localStorage.setItem("username", name);
  };

  // 處理登出，會當成當參數傳給 pages/[userType]Dashboard.js，會連接到某個登出按鈕的點擊事件
  const handleLogout = () => {
    setUserType(null)
    localStorage.removeItem("username");
    localStorage.removeItem("userType");
    localStorage.removeItem("name");
  };


  // 一個網頁程式的回傳值為一整坨像是 HTML 的東西，定義了螢幕上應該出現的樣子，
  // 但這個檔案的回傳值使用了 "react-router-dom" 套件，所以回傳值功能稍微不同。
  // 以下的邏輯大概是:
  // 如果使用者的類別為 A，那就印出 [A]Dashboard.js 的內容，
  // 如果為 null，就印出 LoginPage.js 的內容
  return (
    <Router>
      <Routes>
        {/* 登入頁面 */}
        <Route
          path="/login" // 定義網址後面的路徑
          element={
            userType ? (
              <Navigate to={`/${userType}Dashboard`} replace />
            ) : (
              <LoginPage onLogin={handleLogin} /> // 把登入函數傳給 LoginPage
            )
          }
        />
        {/* 已登入頁面（受保護） */}
        <Route
          path="/CustomerDashboard"
          element={
            <ProtectedRoute userType={userType} allowedType="customer">
              <CustomerDashboard onLogout={handleLogout} /> {/* 把登出函數傳給 CustomerDashboard */}
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
