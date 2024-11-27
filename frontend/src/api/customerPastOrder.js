// 模組化身份驗證的 API，把 API 呼叫封裝成一般的函式
import { apiCall } from "../api";


export const getCustomerPastOrder = async (c_id) => {
  try {
    const response = await apiCall(`/customer/past_orders`, "POST", {c_id});
    return response;
  } catch (error) {
    console.error("Get CustomerPastOrder failed:", error.message);
    throw error;
  }
};

