import { apiCall } from "../api";


export const completeOrder = async (o_id, complete_time) => {
  try {
    const response = await apiCall(`/restaurant/complete/order`, "POST", {o_id, complete_time});
    console.log(response);
    return response;
  } catch (error) {
    console.error("complete order failed:", error.message);
    throw error;
  }
};