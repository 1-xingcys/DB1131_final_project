// src/api.js
const API_BASE_URL = process.env.REACT_APP_BACKEND_URL;

// 通用的 API 函數
export const apiCall = async (endpoint, method = "GET", body = null, headers = {}) => {
  const config = {
    method, // HTTP 方法
    headers: {
      "Content-Type": "application/json", // 默認使用 JSON 格式
      ...headers, // 自定義 headers
    },
  };

  // 如果有請求體，則添加到配置中
  if (body) {
    config.body = JSON.stringify(body);
  }

  try {
    // 發送請求
    const response = await fetch(`${API_BASE_URL}${endpoint}`, config);

    // 處理非成功狀態碼
    if (!response.ok) {
      const errorData = await response.json(); // 解析錯誤訊息
      throw new Error(errorData.message || `Error: ${response.status}`);
    }

    // 返回成功的數據
    return await response.json();
  } catch (error) {
    console.error("API 呼叫錯誤:", error.message);
    throw error; // 將錯誤拋出給上層處理
  }
};
