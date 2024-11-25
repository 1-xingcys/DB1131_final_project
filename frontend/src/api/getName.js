// 模組化取得顧客名字的 API，把 API 呼叫封裝成一般的函式
import { apiCall } from "../api";


export const getName = async (username) => {
  try {
    const response = await apiCall(`/customer/cname`, "POST", {username});
    return response;
  } catch (error) {
    console.error("Get name failed:", error.message);
    throw error;
  }
};