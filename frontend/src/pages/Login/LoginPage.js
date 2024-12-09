import React, {useState} from "react";

// 我已經模組化過的的 API 介面
import { authenticate } from "../../api/auth";
import { getName } from "../../api/getName";

import "../../index.css";
import styles from "./LoginPage.module.css";

// This page has a parameter, a function 'onlogin()' defined in App.js
function LoginPage({ onLogin }) {

  /* 變數宣告 */

  const [selectedRole, setSelectedRole] = useState(""); // 保存選擇的身份
  const [username, setUsername] = useState(
    sessionStorage.getItem("username") || ""
  ) ;// 保存帳號
  const [password, setPassword] = useState("");         // 保存密碼
  const [errorMessage, setErrorMessage] = useState(""); // 錯誤提示


  // 處理身份選擇
  const handleRoleSelect = (e) => {
    setSelectedRole(e.target.value);
    setErrorMessage(""); // 清空錯誤提示
  };

   // 處理登入按鈕點擊
  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!username || !password) {
      setErrorMessage("請輸入帳號和密碼！");
      return;
    }

    // 會確認身份是否正確以及取得使用者名字，總共 call 兩個 API
    try {
      const response = await authenticate(selectedRole, username, password);
      console.log("Authentication successful:", response);
      if (selectedRole === "customer" || selectedRole === "restaurant"){
        try {
          const response = await getName(selectedRole, username);
          sessionStorage.setItem("name", response);
          console.log("get name successful", response);
        } catch (error) {
          console.log("get name failed :", error.message);
        }
      }
      // 呼叫從 App.js 傳來的處理登入的函式
      onLogin(selectedRole, username);
    } catch (error) {
      console.error("Error during authentication:", error.message);
      setErrorMessage("帳號不存在或密碼錯誤！");
    }
  };


  return (
    <div>
      <h1 className={styles.title}>登入</h1>

      {/* 下拉選單選擇身份 */}
      <div className={styles.container}>
        <label htmlFor="role-select"></label>
        <select className={styles.formElement} id="role-select" value={selectedRole} onChange={handleRoleSelect}>
          <option value="">-- 請選擇身份 --</option>
          <option value="restaurant">商家（Restaurant）</option>
          <option value="customer">顧客（Customer）</option>
        </select>
      </div>

      <form onSubmit={handleSubmit}>
        
        {/* 輸入帳號與密碼 */}
        {selectedRole && (
          <div>
            {/* <h3>請輸入帳號與密碼：</h3> */}
            <p>
            <input
              className={styles.formElement}
              type="text"
              placeholder="請輸入帳號"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            </p>
            <p>
            <input
              className={styles.formElement}
              type="password"
              placeholder="請輸入密碼"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            </p>
          </div>
        )}

        {/* 登入按鈕 */}
        <div>
          {selectedRole && (<button className={`${styles.button} ${styles.formElement}`} type="submit">登入</button>)}
        </div>

        {/* 錯誤提示 */}
        {errorMessage && <p className={styles.errorMessage}>{errorMessage}</p>}

      </form>

    </div>
  );
}

export default LoginPage;

