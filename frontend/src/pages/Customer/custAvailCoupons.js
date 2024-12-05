import { useState, useEffect } from "react";
import { getCustomerAvailCoupons } from "../../api/getCustAvailCoupons";

function CustomerAvailCoupons() {
  const [coupons, setCoupons] = useState([]);

  useEffect(() => {
    const fetchCoupons = async () => {
      try {
        const response = await getCustomerAvailCoupons(sessionStorage.getItem("username"));
        setCoupons(response);
        console.log("Get customer available coupons successful", response);
      } catch (error) {
        console.log("Get customer available coupons failed: ", error.message);
      }
    };

    fetchCoupons();
  }, []);

  return (
    <div>
      <h1>可用折價券資訊</h1>

      {/* 動態呈現顧客的可用折價券資訊 */}
      <div>
        {coupons.length > 0 ? (
          coupons.map((coupon) => (
            <div key={coupon.coupon_id} style={{ marginBottom: "20px" }}>
              <h2>折價券編號: {coupon.coupon_id}</h2>
              <p>折扣率: {coupon.discount_rate * 100}%</p>
              <p>開始日期: {coupon.start_date}</p>
              <p>到期日期: {coupon.due_date}</p>
            </div>
          ))
        ) : (
          <p>目前沒有可用的折價券。</p>
        )}
      </div>
    </div>
  );
}

export default CustomerAvailCoupons;

  