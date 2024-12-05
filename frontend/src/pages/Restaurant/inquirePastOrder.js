import {useState, useEffect} from "react"
import { getRestPastOrder } from "../../api/getRestPastOrder";

function RestGetPastOrder() {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const response = await getRestPastOrder(sessionStorage.getItem("username"));
        setOrders(response);
        console.log("get restaurant regular info successful", response);
      } catch (error) {
        console.log("get restaurant regular info failed :", error.message);
      }
    };
  
    fetchOrders();
  }, []);

    return (
        <div>
        <h1>過去訂單資訊</h1>
        {/* 動態生成表格 */}
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
            </tr>
            </thead>
            <tbody>
            {orders.map((order) => (
                <tr key={order.id}>
                <td>{order.id}</td>
                <td>{order.order_time}</td>
                <td>{order.expected_time}</td>
                <td>{order.finish_time}</td>
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
                        {meal.meal_name} x {meal.quantity}
                      </li>
                    ))}
                  </ul>
                </details>
              </td>
                </tr>
            ))}
            </tbody>
        </table>
        </div>
    );
}

export default RestGetPastOrder;