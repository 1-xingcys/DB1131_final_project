import React from "react";


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
    <form>
      <div>
        <label>
          <input
            type="checkbox"
            name="eating_utensil"
            checked={orderInfo.eating_utensil}
            onChange={handleCheckboxChange}
          />
          是否需要免洗餐具
        </label>
      </div>
      <div>
        <label>
          <input
            type="checkbox"
            name="plastic_bag"
            checked={orderInfo.plastic_bag}
            onChange={handleCheckboxChange}
          />
          是否需要塑膠袋
        </label>
      </div>
      <div>
        <label htmlFor="order-note">備註：</label>
        <textarea
          id="order-note"
          value={orderInfo.note}
          onChange={handleNoteChange}
          placeholder="輸入..."
        />
      </div>
    </form>
  );
}

export default OrderDetailsForm;
