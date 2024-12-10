import { apiCall } from "../api";

export const updateReview = async (o_id, review = null, star_num = null) => {
  if (!o_id) {
    throw new Error("o_id is required");
  }
  if (review === null && star_num === null) {
    throw new Error("At least one of review or star_num is required");
  }

  const reviewData = {
    o_id: o_id,
    review: review,
    star_num: star_num,
  };

  try {
    const response = await apiCall(`/customer/update/review`, "POST", reviewData);
    // 根據後端的回應處理特定情況
    if (response.error) {
        if (response.error === "Review or star_num already exists") {
          throw new Error("Review or star_num already exists");
        } if (response.error === "At least one of review or star_num is required") {
            throw new Error("At least one of review or star_num is required");  
        }else {
          throw new Error(response.error || "Unknown error occurred while updating review.");
        }
      }  
    return response; // 成功回應

  } catch (error) {
    console.error("submit review failed:", error);
    throw error;
  }
};
