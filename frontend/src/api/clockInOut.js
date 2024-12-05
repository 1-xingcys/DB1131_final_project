import { apiCall } from "../api";


export const clock_in = async (r_id) => {
  try {
    const response = await apiCall(`/restaurant/clock/in`, "POST", { r_id });
    console.log("Clock in successful");
    return response;
  } catch (error) {
    console.error("Clock in failed:", error.message);
    throw error;
  }
};

export const clock_out = async (r_id) => {
    try {
      const response = await apiCall(`/restaurant/clock/out`, "POST", {r_id});
      console.log("Clock out successful");
      return response;
    } catch (error) {
      console.error("Clock out failed:", error.message);
      throw error;
    }
  };

export const check_clock_in_status = async (r_id) => {
    try {
      const response = await apiCall(`/restaurant/check/clock`, "POST", {r_id});
      console.log("Clocked In!");
      return response;
    } catch (error) {
      console.error("Failed:", error.message);
      throw error;
    }
  };