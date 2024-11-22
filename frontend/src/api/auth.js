// src/api/auth.js
import { apiCall } from "../api";


export const authenticate = async (selectedRole, username, password) => {
  try {
    const response = await apiCall(`/authentication/${selectedRole}`, "POST", {username, password});
    return response;
  } catch (error) {
    throw error;
  }
};