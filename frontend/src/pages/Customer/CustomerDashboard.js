import React, { useState, useEffect } from "react";

// 以下的引用全部都是為了模組化，把以下的功能貼到這個檔案也有一樣的效果，但這樣會很混亂
import CurrentTime from "../../components/time"; // 得到即時時間
import RestRegInfo from "./restRegInfo"; // 取得餐廳 regular 資訊
import OrderForm from "./placeOrder/placeOrder.js"; // 處理訂單
import CustomerPastOrders from "./customerPastOrder"; //顧客歷史訂單
import CustomerAvailCoupons from "./custAvailCoupons"; // 當前可用折價券

import styles from "./CustomerDashboard.module.css";

function CustomerDashboard({ onLogout }) {
  // 這個狀態變數用來判斷現在顧客是要「查看餐廳資訊」還是「立即點餐」
  const [view, setView] = useState("");
  const [isSidebarVisible, setIsSidebarVisible] = useState(true);

  const toggleSidebar = () => {
    setIsSidebarVisible(!isSidebarVisible);
  };

  const handleViewChange = (newView) => {
    if(view === newView){
      setView("");
    }
    else {
      setView(newView);
    }
  };

  return (
    <div style={{ display: 'flex' }}>
      {/* 常駐左上方的按鈕 */}
      <button className={styles.fixedToggleButton} onClick={toggleSidebar}>
        {isSidebarVisible ? "隱藏側邊欄" : "顯示側邊欄"}
      </button>

      {/* 側邊欄 */}
      {isSidebarVisible && (
        <div className={styles.sidebar}>
          <h2 className={styles.helloMessage}>您好 {sessionStorage.getItem("name")} ！</h2>
            <CurrentTime />
          <button className={styles.button} onClick={() => handleViewChange("info")}>
            查看餐廳資訊
          </button>
          <button className={styles.button} onClick={() => handleViewChange("order")}>
            立即點餐
          </button>
          <button className={styles.button} onClick={() => handleViewChange("past")}>
            查看已完成訂單
          </button>
          <button className={styles.button} onClick={() => handleViewChange("processing")}>
            查看處理中訂單
          </button>
          <button className={styles.button} onClick={() => handleViewChange("coupon")}>
            查看可用折價券
          </button>
          <button className={styles.logoutButton} onClick={onLogout}>
            登出
          </button>
        </div>
      )}

      {/* 主內容區域 */}
      <div style={{ flex: 1, padding: '20px' }}> 
        {view === "info" && <RestRegInfo />}
        {view === "order" && <OrderForm />}
        {view === "past" && <CustomerPastOrders view={view} />}
        {view === "processing" && <CustomerPastOrders view={view} />}
        {view === "coupon" && <CustomerAvailCoupons />}
      </div>
    </div>
  );
}

export default CustomerDashboard;