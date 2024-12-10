import React, { useState, useEffect } from "react";
import { get_serve_meal_status } from "../../api/updateServeMeal"; 

import styles from "./RestaurantDashboard.module.css";

function ServeStatus({ isClockIn, onBack }) {
  const [serveMealData, setServeMealData] = useState([]);
  const [loading, setLoading] = useState(true); // 加載狀態
  const [error, setError] = useState(null); // 錯誤信息

  // 獲取今日供應狀況及剩餘份數
  useEffect(() => {
    const fetchServeMealData = async () => {
      try {
        setLoading(true);
        const r_id = sessionStorage.getItem("username"); // 獲取餐廳 ID
        const response = await get_serve_meal_status(r_id); 
        setServeMealData(response); // 保存數據
      } catch (error) {
        console.error("Failed to fetch serve meal status:", error.message);
        setError("無法加載品項供應情形，請稍後再試！");
      } finally {
        setLoading(false);
      }
    };

    fetchServeMealData();
  }, []);

  // 返回的頁面結構
  return (
    <div className={styles.container}>
      <h1>今日品項供應情形</h1>

      {loading && <p className={styles.loading}>正在加載數據...</p>}
      {error && <p className={styles.error}>{error}</p>}

      {!loading && !error && (
        <table className={styles.table}>
          <thead>
            <tr>
              <th>品項名稱</th>
              <th>今日供應量</th>
              <th>今日剩餘份數</th>
            </tr>
          </thead>
          <tbody>
            {serveMealData.length > 0 ? (
              serveMealData.map((item, index) => (
                <tr key={index}>
                  <td>{item.name}</td>
                  <td>{item.supply_num}</td>
                  <td>{item.remaining_num}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="3" style={{ textAlign: "center" }}>
                  暫無供應數據
                </td>
              </tr>
            )}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default ServeStatus;