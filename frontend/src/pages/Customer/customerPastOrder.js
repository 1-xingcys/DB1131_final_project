import {useState, useEffect} from "react"
import { getCustomerPastOrder } from "../../api/getCustPastOrder";
import { NULL_TIME_STAMP } from "../../components/constant";

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

        <h1>{view === "past" ? "已完成訂單" : "處理中訂單"}</h1>
  
        {/* 動態呈現顧客的歷史訂單資訊 */}
        <div>
          {orders.map((order) => (
            <div key={order.order_id} style={{ marginBottom: "20px" }}>
              <h2>訂單號碼: {order.order_id}</h2>
              <p>餐廳名稱: {order.restaurant_name}</p>
              <p>訂單時間: {order.order_time}</p>
              <p>預計取餐時間: {order.expected_time}</p>
              <p>{(order.pick_up_time !== NULL_TIME_STAMP) && `取餐時間: ${order.pick_up_time}`}</p>
              <p>是否需要餐具: {order.eating_utensil ? "是" : "否"}</p>
              <p>是否需要塑膠袋: {order.plastic_bag ? "是" : "否"}</p>
              <p>備註: {order.note || "無"}</p>

  
              {/* 顯示餐點資訊 */}
              <h3>餐點列表：</h3>
              <ul>
                {order.meals.map((meal, index) => (
                  <li key={index}>
                    {meal.name} - 數量: {meal.number}
                  </li>
                ))}
              </ul>
              {/* 顯示折價券資訊 */}
            <p>
              使用折價券種類:{" "}
              {order.discount_rate ? `${order.discount_rate * 100}% 折扣` : "無使用折價券"}
            </p>
            {/* 顯示總金額 */}
            <p>總金額: ${order.total_price ? order.total_price.toFixed(2) : "計算中"}</p>
         
            </div>
          ))}
        </div>
      </div>
    );
  }
  
  export default CustomerPastOrders;
  