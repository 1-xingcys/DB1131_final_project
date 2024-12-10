import { useState, useEffect } from "react"
import { updateReview } from "../../api/updateReview";


function WriteNote({ order, setIsWritingNote }) {
    const [reviews, setReviews] = useState({}); // 儲存每個訂單的評論和星數

    useEffect(() => {

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
            alert("提交失敗，請稍後再試。");
        } finally {
            setIsWritingNote(false);
        }
    };

    return (
    <div>
        {/* 評論輸入框 */}
        <div>
          <label>
            評論：
            <input
              type="text"
              value={reviews[order.order_id]?.review || ""}
              onChange={ (e) => handleReviewChange(order.order_id, e.target.value) }
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
              onClick={() => handleStarClick(order.order_id, star)}
            >★</span>
          ))}
        </div>

        {/* 提交按鈕 */}
        <button
          onClick={() => handleSubmit(order.order_id)}
        >
          提交評價
        </button>
        <button onClick={() => setIsWritingNote(false)}>返回</button>
    </div>
    );
}


export default WriteNote