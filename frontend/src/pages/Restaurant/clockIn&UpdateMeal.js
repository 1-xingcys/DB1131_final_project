import React, { useState, useEffect } from "react";
import { clock_in } from "../../api/clockInOut"; // 導入 clock_in 函數
import { update_serve_meal } from "../../api/updateServeMeal";
import { getRestMealItem } from "../../api/restMealItem";
import { check_serve_meal_status } from "../../api/updateServeMeal";

import styles from "./restOther.module.css"; // 引入樣式模組


function ClockIn({ setIsWorking, onBack }) {
  const [meals, setMeals] = useState([]); // 存放店家品項資訊
  const [supplyNums, setSupplyNums] = useState({}); // 存放每個品項的供應量
  const [isUpdating, setIsUpdating] = useState(false); // 是否正在更新供應量
  const [isUpdated, setIsUpdated] = useState(false); // 是否完成供應量更新
  
  const r_id = sessionStorage.getItem("username");
  
  // 獲取商家的所有品項＋檢查當天是否已更新
  useEffect(() => {
    const fetchMealsAndCheckStatus = async () => {
      try {
        // 獲取品項
        const mealResponse = await getRestMealItem(r_id);
        setMeals(mealResponse);

        const initialSupplyNums = mealResponse.reduce((acc, meal) => {
          acc[meal.name] = meal.supply_num || 0;
          return acc;
        }, {});
        setSupplyNums(initialSupplyNums);

        // 檢查供應量狀態
        const statusResponse = await check_serve_meal_status(r_id);
        if (typeof statusResponse === "boolean") {
          setIsUpdated(statusResponse); // 確認是否已經更新過供應量
        } else {
          console.error("Unexpected response format from check_serve_meal_status");
          setIsUpdated(false);
        }
        
      } catch (error) {
        console.error("Failed to fetch meals or check status:", error.message);
      }
    };

    if (r_id) 
      fetchMealsAndCheckStatus();
    
  }, [r_id]);


  // 更新供應量
  const handleUpdateSupplies = async () => {
    setIsUpdating(true);
    try {
      for (const meal of meals) {
        const name = meal.name;
        const supply_num = supplyNums[name];
        await update_serve_meal(r_id, name, supply_num); // 調用 API 更新供應量
      }
      setIsUpdated(true);
      alert("供應量更新成功 (๑╹◡╹๑)");
    } catch (error) {
      console.error("更新供應量失敗:", error.message);
      alert("更新失敗 இдஇ，請稍後再試！");
    } finally {
      setIsUpdating(false);
    }
  };

  // 確認打卡
  const handleClockIn = async () => {
    try {
      await clock_in(r_id); // 調用打卡 API
      alert("打卡成功 ✧*｡٩(ˊᗜˋ*)و✧*｡！");
      setIsWorking(true); // 更新打卡狀態
      onBack(); // 返回 Dashboard
    } catch (error) {
      console.error("打卡失敗:", error.message);
      alert("上班失敗 (๑•ૅㅁ•ૅ๑)，請稍後再試！");
    }
  };


  return (
    <div className={styles.tableContainer}>
      <h2>更新供應量</h2>
      <table className={styles.table}>
        <thead>
          <tr>
            <th>品項</th>
            <th>數量</th>
          </tr>
        </thead>
        <tbody>
          {meals.map((meal, index) => (
            <tr key={index}>
              <td>{meal.name}</td>
              <td>
                <input
                  type="number"
                  value={supplyNums[meal.name] || ""}
                  onChange={(e) =>
                    setSupplyNums({
                      ...supplyNums,
                      [meal.name]: parseInt(e.target.value, 10),
                    })
                  }
                  disabled={isUpdated}
                />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className={styles.buttonContainer}>
        <button
          className={styles.button}
          onClick={handleUpdateSupplies}
          disabled={isUpdated || isUpdating}
        >
          更新供應量
        </button>

        {/* 確認打卡按鈕 */}
        {isUpdated && (
          <button className={styles.button} onClick={handleClockIn}>
            開啟值班
          </button>
        )}
        
        <button className={styles.button} onClick={onBack}>
          返回
        </button>
      </div>
    </div>
  );
}

export default ClockIn;
