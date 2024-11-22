import React from "react";
import { Navigate } from "react-router-dom";

function ProtectedRoute({ userType, allowedType, children }) {
  if (!userType) {
    // 未登入，跳轉到登入頁面
    return <Navigate to="/login" replace />;
  }

  if (userType !== allowedType) {
    // 使用者類型不符合，禁止訪問
    return <Navigate to="/login" replace />;
  }

  // 符合條件，渲染內容
  return children;
}

export default ProtectedRoute;
