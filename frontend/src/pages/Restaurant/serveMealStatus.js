import React, { useState, useEffect } from "react";
import { get_serve_meal_status } from "../../api/updateServeMeal"; // API 函數

function ServeStatus({ isClockIn, onBack }) {
  const [serveMealData, setServeMealData] = useState([]);
  const [loading, setLoading] = useState(true); // 加載狀態
  const [error, setError] = useState(null); // 錯誤信息

  // 當組件加載時調用 API 獲取數據
  useEffect(() => {
    const fetchServeMealData = async () => {
      try {
        setLoading(true);
        const r_id = sessionStorage.getItem("username"); // 獲取餐廳 ID
        const response = await get_serve_meal_status(r_id); // 調用 API
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
    <div>
      <h2>今日品項供應情形</h2>

      {/* 加載中狀態 */}
      {loading && <p>正在加載數據...</p>}

      {/* 錯誤信息 */}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {/* 表格展示供應數據 */}
      {!loading && !error && (
        <table border="1" cellPadding="5" style={{ borderCollapse: "collapse", width: "100%" }}>
          <thead>
            <tr>
              <th>品項名稱</th>
              <th>供應量</th>
            </tr>
          </thead>
          <tbody>
            {serveMealData.length > 0 ? (
              serveMealData.map((item, index) => (
                <tr key={index}>
                  <td>{item.name}</td>
                  <td>{item.supply_num}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="2" style={{ textAlign: "center" }}>
                  暫無供應數據
                </td>
              </tr>
            )}
          </tbody>
        </table>
      )}

      {/* 返回按鈕 */}
      {/* <button onClick={onBack} style={{ marginTop: "20px" }}>
        返回
      </button> */}
    </div>
  );
}

export default ServeStatus;