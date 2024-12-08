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

export const check_serve_meal_status = async (r_id) => {
  try {
    const response = await apiCall(`/restaurant/check/serve/meal`, "POST", { r_id });
    console.log(`Check serve status successful`);
    return response;
  } catch (error) {
    console.error(`Checked failed:`, error.message);
    throw error;
  }
};

export const get_serve_meal_status = async (r_id) => {
  try {
    const response = await apiCall(`/restaurant/get/serve/meal`, "POST", { r_id });
    console.log(`Check serve status successful`);
    return response;
  } catch (error) {
    console.error(`Checked failed:`, error.message);
    throw error;
  }
};