// 模組化身份驗證的 API，把 API 呼叫封裝成一般的函式
import { apiCall } from "../api";


export const authenticate = async (selectedRole, username, password) => {
  try {
    const response = await apiCall(`/authentication/${selectedRole}`, "POST", {username, password});
    return response;
  } catch (error) {
    console.error("Authentication failed:", error.message);
    throw error;
  }
};