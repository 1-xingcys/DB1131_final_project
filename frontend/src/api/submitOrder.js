import { apiCall } from "../api";


export const submitOrder = async (orderProcessingTime, eating_utensil, plastic_bag, note, c_id, r_id, meal_items) => {
  
  const formatDate = (date) => {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0'); // 月份從 0 開始，需要 +1
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');
    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
  };

  // 生成當下時間
  const now = new Date();
  const afterProcess = new Date(now.getTime() + orderProcessingTime * 60 * 1000);

  const orderData = {
    order_time: formatDate(now),
    expected_time: formatDate(afterProcess),
    pick_up_time: formatDate(afterProcess),
    eating_utensil: eating_utensil,
    plastic_bag: plastic_bag,
    note: note,
    c_id: c_id,
    r_id: r_id,
    meal_items: meal_items,
  };


  try {
    const response = await apiCall(`/customer/submit/order`, "POST", orderData);
    return response;
  } catch (error) {
    console.error("Authentication failed:", error.message);
    throw error;
  }
};