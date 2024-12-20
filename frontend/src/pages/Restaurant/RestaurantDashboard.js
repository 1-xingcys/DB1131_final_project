import React, { useState, useEffect } from "react";

import CheckOrder from "./checkOrder"; 
import ClockIn from "./clockIn&UpdateMeal";
import ClockOut from "./clockOut";
import ServeStatus from "./serveMealStatus";
import { check_clock_in_status } from "../../api/clockInOut";

import styles from "./RestaurantDashboard.module.css"; 



function RestaurantDashboard({ onLogout }) {
  const [isWorking, setIsWorking] = useState(false);// 確認是否上班中
  const [hasClockInRecord, setHasClockInRecord] = useState(false); // 確認今日是否已有打卡紀錄
  const [view, setView] = useState(""); // 這個狀態變數用來判斷現在餐廳的操作
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
        const r_id = sessionStorage.getItem("username"); 
        const response = await check_clock_in_status(r_id); 
        setIsWorking(response.working); 
        setHasClockInRecord(response.isClocked)
      } catch (error) {
        console.error("Failed to fetch clock-in status:", error.message);
      }
    };

    fetchClockInStatus();
  }, []);

  return (
    <div className={styles.restaurantDashboard}>
      {/* 三條線按鈕 */}
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
        <h1 className={styles.helloMessage}>您好 {sessionStorage.getItem("name")} ！</h1>
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
      <div
      className={`${styles.content} ${
        isSidebarVisible ? styles.shifted : ""
      }`}
      >
      <h1 className={styles.title}>真正的餓徒是不排隊的！</h1>
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
        {view === "checkOrder" && <CheckOrder isClockIn={isWorking} />}
        {view === "checkServe" && <ServeStatus isClockIn={isWorking} />}
      </div>
    </div>
    </div>
  );
}

export default RestaurantDashboard;
