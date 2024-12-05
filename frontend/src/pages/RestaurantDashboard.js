import React, { useState, useEffect } from "react";

import PastOrder from "./Restaurant/inquirePastOrder"; // 取得餐廳方歷史訂單資訊
import ClockIn from "./Restaurant/clockIn&UpdateMeal";
import ClockOut from "./Restaurant/clockOut";
import { check_clock_in_status } from "../api/clockInOut";


function RestaurantDashboard({ onLogout }) {
  // 確認是否已打卡
  const [isClockedIn, setIsClockedIn] = useState(false);
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

  // 在組件加載時檢查是否已打卡
  useEffect(() => {
    const fetchClockInStatus = async () => {
      try {
        const r_id = sessionStorage.getItem("r_id"); // 假設 r_id 存儲在 sessionStorage 中
        const response = await check_clock_in_status(r_id); // 調用查詢 API
        setIsClockedIn(response.isClockedIn); // 根據 API 返回值更新狀態
      } catch (error) {
        console.error("Failed to fetch clock-in status:", error.message);
      }
    };

    fetchClockInStatus();
  }, []);


  return (
    <div>
      <h1>Restaurant Dashboard</h1>

      <h1>您好 {sessionStorage.getItem("name")} ！</h1>

      {/* <div>
        {/* 當按鈕被點擊時改變 view 變數的值*/}
        {/* <button onClick={() => handleViewChange("pastOrder")}>查詢歷史訂單</button>
      </div> */} 
      <div>
      {/* 根據是否已打卡渲染按鈕 */}
      {!isClockedIn ? (
        <>
          <button onClick={() => handleViewChange("clockIn")}>打卡上班</button>
        </>
      ) : (
        <>
          <button onClick={() => handleViewChange("currentOrder")}>處理中訂單</button>
          <button onClick={() => handleViewChange("clockOut")}>打卡下班</button>
          <button onClick={() => handleViewChange("checkOrder")}>查詢訂單</button>
        </>
      )}
    </div>

      <div>
        {/* 根據 view 的值印出對應的資訊 */}
        {view === "clockIn" && (
          <ClockIn
          setIsClockedIn={setIsClockedIn}
          onBack={() => setView("")} // 點擊返回時重置視圖
          />
        )}
        {/* {view === "currentOrder" && <div>查詢現有訂單功能</div>} */}
        {view === "checkOrder" && <PastOrder/>}
        {view === "clockOut" && (
          <ClockOut
          setIsClockedIn={setIsClockedIn}
          onBack={() => setView("")} // 點擊返回時重置視圖
          />
        )}
      </div>

      <button onClick={onLogout}>Logout</button>
    </div>
  );
}

export default RestaurantDashboard;
