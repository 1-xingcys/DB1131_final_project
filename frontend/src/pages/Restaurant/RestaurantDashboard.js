import React, { useState, useEffect } from "react";

import PastOrder from "./inquirePastOrder"; // 取得餐廳方歷史訂單資訊
import ClockIn from "./clockIn&UpdateMeal";
import ClockOut from "./clockOut";
import ServeStatus from "./serveMealStatus";
import { check_clock_in_status } from "../../api/clockInOut";

import styles from "./RestaurantDashboard.module.css"; // 引入樣式模組



function RestaurantDashboard({ onLogout }) {
  // 確認是否上班中、
  const [isWorking, setIsWorking] = useState(false);
  const [hasClockInRecord, setHasClockInRecord] = useState(false);
  // 這個狀態變數用來判斷現在餐廳的操作
  const [view, setView] = useState("");
  const [isSidebarVisible, setIsSidebarVisible] = useState(true); // 控制側邊欄的顯示/隱藏

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
        const r_id = sessionStorage.getItem("username"); // 假設 r_id 存儲在 sessionStorage 中
        const response = await check_clock_in_status(r_id); // 調用查詢 API
        setIsWorking(response.working); // 根據 API 返回值更新狀態
        setHasClockInRecord(response.isClocked)
      } catch (error) {
        console.error("Failed to fetch clock-in status:", error.message);
      }
    };

    fetchClockInStatus();
  }, []);

  return (
    <div className={styles.restaurantDashboard}>
      {/* 漢堡菜單按鈕 */}
      <button
        className={styles.hamburgerButton}
        onClick={() => setIsSidebarVisible(!isSidebarVisible)}
      >
        <span></span>
        <span></span>
        <span></span>
      </button>

      {/* 側邊欄 */}
      <div
        className={`${styles.sidebar} ${
          isSidebarVisible ? styles.visible : styles.hidden
        }`}
      >
        {/* <h2>操作選單</h2> */}
        <h3>您好 {sessionStorage.getItem("name")} ！</h3>
        {!isWorking ? (
          <>
            <button
              onClick={() => handleViewChange("clockIn")}
              disabled={hasClockInRecord}
            >
              打卡上班
            </button>
            <button onClick={() => handleViewChange("checkOrder")}>
              查詢訂單
            </button>
          </>
        ) : (
          <>
            <button onClick={() => handleViewChange("clockOut")}>
              打卡下班
            </button>
            <button onClick={() => handleViewChange("checkOrder")}>
              查詢訂單
            </button>
            <button onClick={() => handleViewChange("checkServe")}>
              品項供應情形
            </button>
          </>
        )}
        <button onClick={onLogout}>Logout</button>
      </div>

      {/* 主內容區域 */}
      <div className={styles.content}>
        <h1>Restaurant Dashboard</h1>
        {/* <h2>您好 {sessionStorage.getItem("name")} ！</h2> */}
        <div className={styles.card}>
          {view === "clockIn" && (
            <ClockIn
              setIsWorking={setIsWorking}
              onBack={() => setView("")}
            />
          )}
          {view === "clockOut" && (
            <ClockOut
              setIsWorking={setIsWorking}
              onBack={() => setView("")}
            />
          )}
          {view === "checkOrder" && <PastOrder isClockIn={isWorking} />}
          {view === "checkServe" && <ServeStatus isClockIn={isWorking} />}
        </div>
      </div>
    </div>
  );
}

export default RestaurantDashboard;
