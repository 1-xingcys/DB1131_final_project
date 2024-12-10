import {useState, useEffect} from "react"
import { getCustomerPastOrder } from "../../api/getCustPastOrder";
import { NULL_TIME_STAMP } from "../../components/constant";
import { updateReview } from "../../api/updateReview";

function CustomerPastOrders( { view } ) {
    const [orders, setOrders] = useState([]);
    const [reviews, setReviews] = useState({}); // 儲存每個訂單的評論和星數

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
    const handleReviewChange = (orderId, value) => {
      setReviews((prev) => ({
        ...prev,
        [orderId]: { ...prev[orderId], review: value },
      }));
    };
  
    const handleStarClick = (orderId, starNum) => {
      setReviews((prev) => ({
        ...prev,
        [orderId]: { ...prev[orderId], star_num: starNum },
      }));
    };
  
    const handleSubmit = async (orderId) => {
      const reviewData = reviews[orderId];
      try {
        const response = await updateReview(orderId, reviewData.review, reviewData.star_num);
        if (response.message === "Order updated successfully") {
          alert(`訂單 ${orderId} 的評論和星數已提交成功！`);
        } else if (response.error === "Review or star_num already exists") {
          alert(`訂單 ${orderId} 的評論或星數已存在，無法更新。`);
        } else {
          console.warn(`提交訂單 ${orderId} 時收到未知回應:`, response);
        }
      } catch (error) {
        console.error(`提交訂單 ${orderId} 的評論和星數失敗:`, error);
        alert("提交失敗，請稍後再試。");}
    };
  
  
    return (
      <div>

        <h1>{view === "past" ? "已完成訂單" : "處理中訂單"}</h1>
  
        {/* 動態呈現顧客的歷史訂單資訊 */}
        <div>
          {orders.map((order) => {
            const isEditable = view === "past"; // 僅在已完成訂單中可編輯
            const isSubmittable =
              reviews[order.order_id]?.review || reviews[order.order_id]?.star_num;
            return (

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
         
            {/* 評論輸入框 */}
            <div>
              <label>
                評論：
                <input
                  type="text"
                  value={reviews[order.order_id]?.review || ""}
                  onChange={(e) =>
                    handleReviewChange(order.order_id, e.target.value)
                  }
                  disabled={!isEditable}
                />
              </label>
            </div>

            {/* 星數評價 */}
            <div>
              <p>星數評價：</p>
              {[1, 2, 3, 4, 5].map((star) => (
                <span
                  key={star}
                  style={{
                    cursor: "pointer",
                    color:
                      reviews[order.order_id]?.star_num >= star
                        ? "gold"
                        : "gray",
                  }}
                  onClick={() => isEditable && handleStarClick(order.order_id, star)

                  }
                >
                  ★
                </span>
              ))}
            </div>

            {/* 提交按鈕 */}
            <button
                onClick={() => handleSubmit(order.order_id)}
                disabled={!isEditable || !isSubmittable}
              >
              提交評價
            </button>
          </div>
          );
        })}
        </div>
      </div>
    );
  }
  
  export default CustomerPastOrders;
  