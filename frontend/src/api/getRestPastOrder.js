// 模組化取得顧客名字的 API，把 API 呼叫封裝成一般的函式
import { apiCall } from "../api";


export const getRestPastOrder = async (r_id) => {
  try {
    const response = await apiCall(`/restaurant/past/order`, "POST", {r_id});
    return response;
  } catch (error) {
    console.error("Get past order failed:", error.message);
    throw error;
  }
};