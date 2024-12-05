import { apiCall } from "../api";


export const update_serve_meal = async (r_id, name, supply_num) => {
  try {
    const response = await apiCall(`/restaurant/update/serve/meal`, "POST", { r_id, name, supply_num });
    console.log(`Update ${name} successful`);
    return response;
  } catch (error) {
    console.error(`Update ${name} failed:`, error.message);
    throw error;
  }
};