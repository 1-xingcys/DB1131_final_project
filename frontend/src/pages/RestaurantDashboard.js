import React from "react";

function RestaurantDashboard({ onLogout }) {
  return (
    <div>
      <h1>Restaurant Dashboard</h1>
      <button onClick={onLogout}>Logout</button>
    </div>
  );
}

export default RestaurantDashboard;
