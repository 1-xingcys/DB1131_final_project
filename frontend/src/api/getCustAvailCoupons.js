// 模組化身份驗證的 API，把 API 呼叫封裝成一般的函式
import { apiCall } from "../api";

export const getCustomerAvailCoupons = async (c_id) => {
  try {
    const response = await apiCall(`/customer/available_coupons`, "POST", {c_id});
    return response;
  } catch (error) {
    console.error("Get CustomerAvailCoupon failed:", error.message);
    throw error;
  }
};