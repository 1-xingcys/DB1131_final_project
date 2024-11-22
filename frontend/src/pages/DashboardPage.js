import React from "react";

function DashboardPage({ onLogout }) {
  const handleLogoutClick = () => {
    onLogout();
  };

  return (
    <div>
      <h1>Dashboard</h1>
      <button onClick={handleLogoutClick}>Logout</button>
    </div>
  );
}

export default DashboardPage;
