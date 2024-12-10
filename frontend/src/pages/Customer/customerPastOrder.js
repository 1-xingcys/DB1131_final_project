import { useState, useEffect } from "react"
import { getCustomerPastOrder } from "../../api/getCustPastOrder";
import { NULL_TIME_STAMP } from "../../components/constant";

import styles from "./custOther.module.css";
import WriteNote from "./writeNote";

function CustomerPastOrders({ view }) {
  const [orders, setOrders] = useState([]);
  const [isWritingNote, setIsWritingNote] = useState(false);
  const [writingOrder, setWrtingOrder] = useState({})
  const [isLoading, setIsLoading] = useState(false); // 加載狀態

  useEffect(() => {
    const fetchOrders = async () => {

        setIsLoading(true); // 開始加載
        try {
          console.log("view : ", view);
          const response = await getCustomerPastOrder(sessionStorage.getItem("username"));
          console.log("get customer past orders successful", response);
          setOrders(view === "past" ? response.filter(order => order.pick_up_time !== NULL_TIME_STAMP)
            : response.filter(order => order.pick_up_time === NULL_TIME_STAMP)
          );
        } catch (error) {
          console.log("get customer past orders failed :", error.message);
        } finally {
          setIsLoading(false); // 結束加載
        }
      };

      fetchOrders();
    }, [isWritingNote]);

    const handleWriteNoteButtonClick = (order) => {
      setIsWritingNote(true);
      setWrtingOrder(order);
    }

  return (
    <div>
      {/* 訂單標題 */}
      <h1 className={styles.title}>
        {!isWritingNote && view ? (view === "past" ? "已完成訂單" : "待處理訂單") : ""}
      </h1>

      {isLoading && (
        <div className={styles.loadingContainer}>
          <div className={styles.spinner}></div>
          <p>加載中，請稍候...</p>
        </div>
      )}

      {/* 動態生成表格 */}
      {!isWritingNote && view && !isLoading && (
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
              {view === "past" && (<th>評分</th>)}
              {view === "past" && (<th>評論</th>)}
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
                {view === "past" && (<td> {order.star_num ? order.star_num : 
                  <button className={styles.button} onClick={() => handleWriteNoteButtonClick(order)}>為此訂單評論</button>}</td>)}
                {view === "past" && (<td> {order.review ? order.review : 
                  <button className={styles.button} onClick={() => handleWriteNoteButtonClick(order)}>為此訂單評分</button>}</td>)}
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

      {isWritingNote && <WriteNote order={writingOrder} setIsWritingNote={setIsWritingNote}/>}
    </div>
  );
}

export default CustomerPastOrders;



