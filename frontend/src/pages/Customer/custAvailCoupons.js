import { useState, useEffect } from "react";
import { getCustomerAvailCoupons } from "../../api/getCustAvailCoupons";

import styles from "./custOther.module.css"; // 引入樣式模組

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
      {coupons.length > 0 ? (
        <table className={styles.table}>
          <thead>
            <tr>
              <th>折價券編號</th>
              <th>折扣率</th>
              <th>開始日期</th>
              <th>到期日期</th>
            </tr>
          </thead>
          <tbody>
            {coupons.map((coupon) => (
              <tr key={coupon.coupon_id}>
                <td>{coupon.coupon_id}</td>
                <td>{(coupon.discount_rate * 100)}%</td>
                <td>{new Date(coupon.start_date).toISOString().split("T")[0]}</td>
                <td>{new Date(coupon.due_date).toISOString().split("T")[0]}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p className={styles.noCoupons}>目前沒有可用的折價券。</p>
      )}
    </div>
  );
}

export default CustomerAvailCoupons;

  