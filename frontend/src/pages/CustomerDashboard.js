import React, { useState, useEffect } from "react";

// 以下的引用全部都是為了模組化，把以下的功能貼到這個檔案也有一樣的效果，但這樣會很混亂
import CurrentTime from "../components/time"; // 得到即時時間
import RestRegInfo from "./Customer/restRegInfo"; // 取得餐廳 regular 資訊
import OrderForm from "./Customer/orderBody"; // 處理訂單
import CustomerPastOrders from "./Customer/customerPastOrder"; //顧客歷史訂單
import CustomerAvailCoupons from "./Customer/custAvailCoupons"; // 當前可用折價券

function CustomerDashboard({ onLogout }) {
  // 這個狀態變數用來判斷現在顧客是要「查看餐廳資訊」還是「立即點餐」
  const [view, setView] = useState("");

  const handleViewChange = (newView) => {
    if(view === newView){
      setView("");
    }
    else {
      setView(newView);
    }
  };

  return (
    <div>
      {/* 取得顧客的名字，此全域變數在登入時已設定好，詳見 LoginPage.js */}
      <h1>您好 {sessionStorage.getItem("name")} ！</h1>

      <div>
        {/* 直接使用在 /components/time.js 定義好的函式*/}
        <CurrentTime/>
      </div>

      <div>
        {/* 當按鈕被點擊時改變 view 變數的值*/}
        <button onClick={() => handleViewChange("info")}>查看餐廳資訊</button>
        <button onClick={() => handleViewChange("order")}>立即點餐</button>
        <button onClick={() => handleViewChange("past")}>查看已完成訂單</button>
        <button onClick={() => handleViewChange("processing")}>查看處理中訂單</button>
        <button onClick={() => handleViewChange("coupon")}>查看可用折價券</button>
      </div>

      <div>
        {/* 根據 view 的值印出對應的資訊 */}
        {view === "info" && <RestRegInfo/>}
        {view === "order" && <OrderForm/>}
        {view === "past" && <CustomerPastOrders view={view}/>}
        {view === "processing" && <CustomerPastOrders view={view}/>}
        {view === "coupon" && <CustomerAvailCoupons/>}

      </div>

      {/* 登出按鈕按下去時會呼叫 onLogout，是 App.js 傳進來的參數 */}
      <button onClick={onLogout}>Logout</button>
    </div>
  );
}

export default CustomerDashboard;
