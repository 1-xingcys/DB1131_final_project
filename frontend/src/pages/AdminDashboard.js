import React from "react";

function AdminDashboard({ onLogout }) {
  return (
    <div>
      <h1>Admin Dashboard</h1>
      <button onClick={onLogout}>Logout</button>
    </div>
  );
}

export default AdminDashboard;
