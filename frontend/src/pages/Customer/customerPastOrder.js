import {useState, useEffect} from "react"
import { getCustomerPastOrder } from "../../api/customerPastOrder";

function CustomerPastOrders() {
    const [orders, setOrders] = useState([]);
  
    useEffect(() => {
      const fetchOrders = async () => {
        try {
          const response = await getCustomerPastOrder(localStorage.getItem("username"));
          setOrders(response.past_orders);
          console.log("get customer past orders successful", response);
        } catch (error) {
          console.log("get customer past orders failed :", error.message);
        }
      };
  
      fetchOrders();
    }, []);
  
    return (
      <div>
        <h1>歷史訂單資訊</h1>
  
        {/* 動態呈現顧客的歷史訂單資訊 */}
        <div>
          {orders.map((order) => (
            <div key={order.order_id} style={{ marginBottom: "20px" }}>
              <h2>訂單號碼: {order.order_id}</h2>
              <p>餐廳名稱: {order.restaurant_name}</p>
              <p>訂單時間: {order.order_time}</p>
              <p>預計取餐時間: {order.expected_time}</p>
              <p>取餐時間: {order.pick_up_time}</p>
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
            </div>
          ))}
        </div>
      </div>
    );
  }
  
  export default CustomerPastOrders;
  