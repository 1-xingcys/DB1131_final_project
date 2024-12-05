import { apiCall } from "../api";
import { NULL_TIME } from "../components/constant";
import { formatDate } from "../components/formatDate";


export const submitOrder = async (orderProcessingTime, eating_utensil, plastic_bag, note, c_id, r_id, meal_items) => {
  // 生成當下時間
  const now = new Date();
  const afterProcess = new Date(now.getTime() + orderProcessingTime * 60 * 1000);

  const orderData = {
    order_time: formatDate(now),
    expected_time: formatDate(afterProcess),
    pick_up_time: NULL_TIME,
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