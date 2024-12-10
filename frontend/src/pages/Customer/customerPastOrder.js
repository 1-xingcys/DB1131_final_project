import {useState, useEffect} from "react"
import { getCustomerPastOrder } from "../../api/getCustPastOrder";
import { NULL_TIME_STAMP } from "../../components/constant";

import styles from "./custOther.module.css"; // 引入樣式模組

function CustomerPastOrders( { view } ) {
    const [orders, setOrders] = useState([]);
  
    useEffect(() => {
      const fetchOrders = async () => {
        try {
          console.log("view : ", view);
          const response = await getCustomerPastOrder(sessionStorage.getItem("username"));
          console.log("get customer past orders successful", response);
          setOrders(view === "past" ? response.filter(order => order.pick_up_time !== NULL_TIME_STAMP)
           : response.filter(order => order.pick_up_time === NULL_TIME_STAMP)
          );
        } catch (error) {
          console.log("get customer past orders failed :", error.message);
        }
      };
  
      fetchOrders();
    }, []);
  
    return (
      <div>
        {/* 訂單標題 */}
        <h1 className={styles.title}>
          {view ? (view === "past" ? "已完成訂單" : "待處理訂單") : ""}
        </h1>
  
        {/* 動態生成表格 */}
        {view && (
          <table className={styles.table}>
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
                <th>折價</th>
              </tr>
            </thead>
            <tbody>
              {orders.map((order) => (
                <tr key={order.order_id}>
                  <td>{order.order_id}</td>
                  <td>
                    {new Date(order.order_time)
                      .toISOString()
                      .replace("T", " ")
                      .slice(0, 16)}
                  </td>
                  <td>
                    {new Date(order.expected_time)
                      .toISOString()
                      .replace("T", " ")
                      .slice(0, 16)}
                  </td>
                  <td>
                    {order.pick_up_time === NULL_TIME_STAMP
                      ? "待處理"
                      : new Date(order.pick_up_time)
                          .toISOString()
                          .replace("T", " ")
                          .slice(0, 16)}
                  </td>
                  <td>{order.eating_utensil ? "✅" : "❌"}</td>
                  <td>{order.plastic_bag ? "✅" : "❌"}</td>
                  <td>{order.note || "無"}</td>
                  <td>{order.c_id}</td>
                  <td>{order.starnum}</td>
                  <td>{order.review || "無"}</td>
                  <td>
                    <details className={styles.details}>
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
                    <td>{order.discount_rate ? `${order.discount_rate * 100}%` : "無"}</td>
                  </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    );
  }
  
  export default CustomerPastOrders;
  