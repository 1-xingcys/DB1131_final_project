import { useState, useEffect } from "react";
import { getRestPastOrder } from "../../api/getRestPastOrder";
import { NULL_TIME_STAMP } from "../../components/constant";
import { completeOrder } from "../../api/completeOrder";
import { formatDate } from "../../components/formatDate";

function CheckOrder( {isClockIn}) {
  const [orders, setOrders] = useState([]);
  const [view, setView] = useState(""); // 訂單視圖

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const response = await getRestPastOrder(sessionStorage.getItem("username"));
        console.log("get restaurant regular info successful", response);

        setOrders(
          view === "past"
            ? response.filter(order => order.finish_time !== NULL_TIME_STAMP)
            : response.filter(order => order.finish_time === NULL_TIME_STAMP)
        );
      } catch (error) {
        console.log("get restaurant regular info failed:", error.message);
      }
    };

    fetchOrders();
  }, [view]);

  const handleConfirm = async (o_id) => {
    try {
      const now = new Date();
      await completeOrder(o_id, formatDate(now));
      setView("");
      alert(`訂單 ${o_id} 已完成`);
    } catch (error) {
      console.error(`完成訂單失敗:`, error.message);
      alert("完成訂單時出現錯誤，請稍後再試");
    }
  };

  const handleViewChange = (newView) => {
    setView(prev => (prev === newView ? "" : newView)); // 切換視圖
  };

  return (
    <div>
      {isClockIn && (<button onClick={() => handleViewChange("processing")}>待處理訂單</button>)}
      <button onClick={() => handleViewChange("past")}>已完成訂單</button>
      <h1>{(view) && (view === "past" ? "已完成訂單" : "待處理訂單")}</h1>

      {/* 動態生成表格 */}
      {view &&
      <table border="1" style={{ borderCollapse: "collapse", width: "100%" }}>
        <thead>
          <tr>
            <th>ID</th>
            <th>訂餐時間</th>
            <th>預期完成時間</th>
            <th>完成時間</th>
            <th>餐具</th>
            <th>塑膠袋</th>
            <th>備註</th>
            <th>顧客ID</th>
            <th>評分</th>
            <th>評論</th>
            <th>餐點</th>
            {view === "processing" && (<th>完成訂單</th>)}
          </tr>
        </thead>
        <tbody>
          {orders.map(order => (
            <tr key={order.id}>
              <td>{order.id}</td>
              <td>{order.order_time}</td>
              <td>{order.expected_time}</td>
              <td>{order.finish_time === NULL_TIME_STAMP ? "待處理" : order.finish_time}</td>
              <td>{order.eating_utensil ? "✅" : "❌"}</td>
              <td>{order.plastic_bag ? "✅" : "❌"}</td>
              <td>{order.note || "無"}</td>
              <td>{order.c_id}</td>
              <td>{order.starnum}</td>
              <td>{order.review || "無"}</td>
              <td>
                {/* 餐點展開 */}
                <details>
                  <summary>訂單細節</summary>
                  <ul>
                    {order.meals.map((meal, index) => (
                      <li key={index}>
                        {meal.name} x {meal.number}
                      </li>
                    ))}
                  </ul>
                </details>
              </td>
              <td>
                {view === "processing" && (
                  <button onClick={() => handleConfirm(order.id)}>完成</button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table> }
    </div>
  );
}

export default CheckOrder;
