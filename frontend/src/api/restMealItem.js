import { apiCall } from "../api";


export const getRestMealItem = async (id) => {
  try {
    const response = await apiCall(`/restaurant/meal_item/regular`, "POST", {id});
    console.log (`Get ${id} meal item successful`, response);
    return response;
  } catch (error) {
    console.error(`Get ${id} meal item failed:`, error.message);
    throw error;
  }
};