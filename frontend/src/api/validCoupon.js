// 模組化身份驗證的 API，把 API 呼叫封裝成一般的函式
import { apiCall } from "../api";


export const validateCoupon = async (c_id, discount_rate) => {
  try {
    const response = await apiCall(`/customer/submit/order/validate/coupon`, "POST", {
        c_id, discount_rate});
    console.log(response);
    return response;
  } catch (error) {
    if (error.message.includes("401")) {
        console.error("Validate Coupon failed: 無效折價券或不存在");
      } else {
        console.error("Validate Coupon failed: 其他錯誤", error.message);
      }
        console.error("Validate Coupon failed:");
      throw error; // 重新拋出錯誤以便上層處理
  }
};
