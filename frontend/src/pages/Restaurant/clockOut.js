import React from "react";
import { clock_out } from "../../api/clockInOut"; // 導入 clock_in 函數

function ClockOut({ setIsClockedIn, onBack }) {
  const handleClockOut = async () => {
    try {
      const r_id = sessionStorage.getItem("username"); // 假設 r_id 存儲在 sessionStorage 中
      await clock_out(r_id); // 調用打卡 API
      alert("Bye Bye ✧*｡٩(ˊᗜˋ*)و✧*｡");
      setIsClockedIn(false); // 更新打卡狀態
      onBack(); // 返回 Dashboard
    } catch (error) {
      console.error("下班失敗:", error.message);
      alert("下班失敗 இдஇ，請稍後再試！");
    }
  };

  return (
    <div>
      <h2>確認打卡</h2>
      <button onClick={handleClockOut}>關閉值班</button>
      <button onClick={onBack}>返回</button>
    </div>
  );
}

export default ClockOut;
