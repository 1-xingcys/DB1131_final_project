import React from "react";
import { clock_out } from "../../api/clockInOut";

import styles from "./restOther.module.css"; 

function ClockOut({ setIsWorking, onBack }) {
  const handleClockOut = async () => {
    try {
      const r_id = sessionStorage.getItem("username"); 
      await clock_out(r_id);
      alert("Bye Bye ✧*｡٩(ˊᗜˋ*)و✧*｡");
      setIsWorking(false); // 更新打卡狀態
      
      window.location.reload(); // 刷新頁面
      onBack(); // 返回 Dashboard
    } catch (error) {
      console.error("下班失敗:", error.message);
      alert("下班失敗 இдஇ，請稍後再試！");
    }
  };

  return (
    <div className={styles.container}>
      <h2 className={styles.title}>確認打卡</h2>
      <button onClick={handleClockOut} className={styles.button}>
        關閉值班
      </button>
      <button onClick={onBack} className={styles.button}>
        返回
      </button>
    </div>
  );
}

export default ClockOut;
