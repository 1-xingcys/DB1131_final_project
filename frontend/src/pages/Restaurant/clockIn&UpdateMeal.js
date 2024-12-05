import React, { useState, useEffect } from "react";
import { clock_in } from "../../api/clockInOut"; // 導入 clock_in 函數
import { update_serve_meal } from "../../api/updateServeMeal";
import { getRestMealItem } from "../../api/restMealItem";

const r_id = sessionStorage.getItem("username");

function ClockIn({ setIsClockedIn, onBack }) {
  const [meals, setMeals] = useState([]); // 存放店家品項資訊
  const [supplyNums, setSupplyNums] = useState({}); // 存放每個品項的供應量
  const [isUpdating, setIsUpdating] = useState(false); // 是否正在更新供應量
  const [isUpdated, setIsUpdated] = useState(false); // 是否完成供應量更新

  // 獲取商家的所有品項
  useEffect(() => {
    const fetchMeals = async () => {
      try {
        const response = await getRestMealItem(r_id); // 調用 API 獲取品項
        setMeals(response); // 保存品項數據到狀態
        const initialSupplyNums = response.reduce((acc, meal) => {
          acc[meal.name] = meal.supply_num || 0; // 初始化供應量
          return acc;
        }, {});
        setSupplyNums(initialSupplyNums);
      } catch (error) {
        console.error("Failed to fetch meals இдஇ:", error.message);
      }
    };

    fetchMeals();
  }, []);

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
      setIsClockedIn(true); // 更新打卡狀態
      onBack(); // 返回 Dashboard
    } catch (error) {
      console.error("打卡失敗:", error.message);
      alert("上班失敗 (๑•ૅㅁ•ૅ๑)，請稍後再試！");
    }
  };

  return (
    <div>
      <h2>更新供應量並打卡上班</h2>

      {/* 列出所有品項及輸入框 */}
      <div>
        {meals.map((meal) => (
          <div key={meal.name}>
            <label>
              {meal.name}:
              <input
                type="number"
                value={supplyNums[meal.name] || ""}
                onChange={(e) =>
                  setSupplyNums({ ...supplyNums, [meal.name]: parseInt(e.target.value, 10) })
                }
              />
            </label>
          </div>
        ))}
      </div>

      {/* 更新供應量按鈕 */}
      <button onClick={handleUpdateSupplies} disabled={isUpdating || isUpdated}>
        更新供應量
      </button>

      {/* 確認打卡按鈕（只有在供應量更新完成後可見） */}
      {isUpdated && (
        <button onClick={handleClockIn}>
          開啟值班
        </button>
      )}

      <button onClick={onBack}>返回</button>
    </div>
  );
}

export default ClockIn;
