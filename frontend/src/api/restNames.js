import { apiCall } from "../api";


export const getRestName = async () => {
  try {
    const response = await apiCall(`/restaurant/name/opening`, "GET");
    console.log("Get Restaurant Names successful");
    return response;
  } catch (error) {
    console.error("Get Restaurant Names failed:", error.message);
    throw error;
  }
};