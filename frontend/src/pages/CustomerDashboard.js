import React, { useState } from "react";
import CurrentTime from "../components/time";
import RestRegInfo from "./Customer/restRegInfo";
import OrderForm from "./Customer/orderBody";

function CustomerDashboard({ onLogout }) {
  const [view, setView] = useState("");


  const handleViewChange = (newView) => {
    setView(newView);
  };


  return (
    <div>
      <h1>您好 {localStorage.getItem("username")} ！</h1>

      <div>
        <CurrentTime/>
      </div>

      <div>
        <button onClick={() => handleViewChange("info")}>查看餐廳資訊</button>
        <button onClick={() => handleViewChange("order")}>立即點餐</button>
      </div>

      <div>
        {view === "info" && <RestRegInfo/>}
        {view === "order" && <OrderForm/>}
      </div>


      <button onClick={onLogout}>Logout</button>
    </div>
  );
}

export default CustomerDashboard;
