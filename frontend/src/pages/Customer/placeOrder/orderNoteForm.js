import React from "react";

import styles from './placeOrder.module.css';


// 處理是否需要餐具、塑膠袋、備註的邏輯
function OrderDetailsForm({ orderInfo, onOrderInfoChange }) {
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
    </form>
  );
}

export default OrderDetailsForm;
