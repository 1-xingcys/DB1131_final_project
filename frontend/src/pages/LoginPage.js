import React, {useState} from "react";
import { authenticate } from "../api/auth";

// This page has a parameter, a function 'onlogin()' defined in App.js
function LoginPage({ onLogin }) {

  /* 變數宣告 */

  const [selectedRole, setSelectedRole] = useState(""); // 保存選擇的身份
  const [username, setUsername] = useState(
    localStorage.getItem("username") || ""
  ) ;// 保存帳號
  const [password, setPassword] = useState("");         // 保存密碼
  const [errorMessage, setErrorMessage] = useState(""); // 錯誤提示
  // const [response, setResponse] = useState("");


  // 處理身份選擇
  const handleRoleSelect = (e) => {
    setSelectedRole(e.target.value);
    setErrorMessage(""); // 清空錯誤提示
  };

   // 處理登入按鈕點擊
  const handleSubmit = () => {
    if (!username || !password) {
      setErrorMessage("請輸入帳號和密碼！");
      return;
    }

    // 暫時的模擬身份驗證
    if (username !== "B10705009" || password !== "1234567Chiu") {
      setErrorMessage("密碼錯誤！");
      return;
    }

    // try {
    //   // 調用後端 API 進行身份驗證
    //   const { token, user } = authenticate(selectedRole, username, password);

    //   // 模擬登入成功，回傳身份
    //   onLogin(selectedRole);
    // } catch (error) {
    //   setErrorMessage(error.message || "登入失敗");
    // }

    onLogin(selectedRole, username);
  };


  return (
    <div>
      <form onSubmit={handleSubmit}>
        <h1>Login Page</h1>

        {/* 下拉選單選擇身份 */}
        <div>
          <label htmlFor="role-select">選擇登入身份：</label>
          <select id="role-select" value={selectedRole} onChange={handleRoleSelect}>
            <option value="">-- 請選擇身份 --</option>
            <option value="Admin">Admin</option>
            <option value="Restaurant">Restaurant</option>
            <option value="Customer">Customer</option>
          </select>
        </div>

        
        {/* 輸入帳號與密碼 */}
        {selectedRole && (
          <div>
            {/* <h3>請輸入帳號與密碼：</h3> */}
            <p>
            <input
              type="text"
              placeholder="請輸入帳號"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
            </p>
            <p>
            <input
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
          {selectedRole && (<button type="submit">登入</button>)}
        </div>

        {/* 錯誤提示 */}
        {errorMessage && <p>{errorMessage}</p>}

      </form>

    </div>
  );
}

export default LoginPage;

