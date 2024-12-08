import React, { useState } from "react";

import styles from './placeOrder.module.css';
import { validateCoupon } from "../../../api/validCoupon";

// 處理是否需要餐具、塑膠袋、備註的邏輯
function OrderDetailsForm({ orderInfo, onOrderInfoChange }) {
  const[selectedDiscountRate, setSelectedDiscountRate] = useState("");
  const [couponId, setCouponId] = useState(null); // 用於存儲驗證成功的 coupon_id

  // 處理勾選框變化
  const handleCheckboxChange = (e) => {
    const { name, checked } = e.target;
    onOrderInfoChange({ ...orderInfo, [name]: checked });
  };

  // 處理備註變化
  const handleNoteChange = (e) => {
    const { value } = e.target;
    onOrderInfoChange({ ...orderInfo, note: value });
  };
  // 處理折扣率選擇變化
  const handleDiscountRateChange = async (e) => {
    setSelectedDiscountRate(e.target.value);
    try {
      const result = await validateCoupon(sessionStorage.getItem("username"), e.target.value);
      setCouponId(result);
      onOrderInfoChange({ ...orderInfo, coupon_id: result});
    } catch(error){
      console.log("handleDiscountRateChange出包");
      console.error("無法驗證折價券:", error?.response?.error || "未知錯誤");
      alert("折價券驗證失敗，請到左攔查看現有折價券！");
      setSelectedDiscountRate("");
    }

  };
  return (
    <form className={styles.formContainer}>
      <div className={styles.formGroup}>
        <label  className={styles.checkboxLabel}>
          <input
            type="checkbox"
            name="eating_utensil"
            checked={orderInfo.eating_utensil}
            onChange={handleCheckboxChange}
            className={styles.checkboxInput}
          />
          是否需要免洗餐具
        </label>
      </div>
      <div className={styles.formGroup}>
        <label className={styles.checkboxLabel}>
          <input
            type="checkbox"
            name="plastic_bag"
            checked={orderInfo.plastic_bag}
            onChange={handleCheckboxChange}
            className={styles.checkboxInput}
          />
          是否需要塑膠袋
        </label>
      </div>
      <div className={styles.formGroup}>
        <label htmlFor="order-note" className={styles.textareaLabel}>
          備註：
        </label>
        <textarea
          id="order-note"
          value={orderInfo.note}
          onChange={handleNoteChange}
          placeholder="輸入..."
          className={styles.textarea}
        />
      </div>
      <div className={styles.formGroup}>
        <label htmlFor="discount-rate-select" className={styles.dropdownLabel}>
          選擇折扣：
        </label>
        <select
          id="discount-rate-select"
          value={selectedDiscountRate}
          onChange={handleDiscountRateChange}
          className={styles.dropdown}
        >
          <option value="">-- 不使用折價券 --</option>
          <option value="0.7">七折</option>
          <option value="0.75">七五折</option>
          <option value="0.8">八折</option>
          <option value="0.85">八五折</option>
          <option value="0.9">九折</option>
          {!couponId && <p>沒有折扣率 {selectedDiscountRate} 的折價券，請到左攔查看現有折價券</p>}
        </select>
      </div>
    </form>
  );
}

export default OrderDetailsForm;
