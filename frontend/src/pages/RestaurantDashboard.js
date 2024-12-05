import React, { useState, useEffect } from "react";

import PastOrder from "./Restaurant/inquirePastOrder"; // 取得餐廳方歷史訂單資訊

function RestaurantDashboard({ onLogout }) {
  // 這個狀態變數用來判斷現在餐廳的操作
  const [view, setView] = useState("");
  const handleViewChange = (newView) => {
    if(view === newView){
      setView("");
    }
    else {
      setView(newView);
    }
  };


  return (
    <div>
      <h1>Restaurant Dashboard</h1>

      <h1>您好 {sessionStorage.getItem("name")} ！</h1>

      <div>
        {/* 當按鈕被點擊時改變 view 變數的值*/}
        <button onClick={() => handleViewChange("pastOrder")}>查詢歷史訂單</button>
      </div>

      <div>
        {/* 根據 view 的值印出對應的資訊 */}
        {view === "pastOrder" && <PastOrder/>}
      </div>

      <button onClick={onLogout}>Logout</button>
    </div>
  );
}

export default RestaurantDashboard;
