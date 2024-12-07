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

export const getRestAvailableMealItem = async (id) => {
  try {
    const response = await apiCall(`/restaurant/meal_item/available`, "POST", {id});
    console.log (`Get ${id} available meal item successful`, response);
    return response;
  } catch (error) {
    console.error(`Get ${id} available meal item failed:`, error.message);
    throw error;
  }
};