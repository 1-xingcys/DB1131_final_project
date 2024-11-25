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