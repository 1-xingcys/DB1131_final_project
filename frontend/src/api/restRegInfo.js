// 模組化取得餐廳 Regular 資訊的 API，把 API 呼叫封裝成一般的函式
import { apiCall } from "../api";

export const getRestRegInfo = async () => {
  try {
    const response = await apiCall(`/restaurant/info/regular`, "GET");
    return response;
  } catch (error) {
    console.error("get restaurant regular info failed:", error.message);
    throw error;
  }
};