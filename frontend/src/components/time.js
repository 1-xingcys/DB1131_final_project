import React, { useState, useEffect } from "react";

function CurrentTime() {
  const [time, setTime] = useState("");

  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      const hours = String(now.getHours()).padStart(2, "0");
      const minutes = String(now.getMinutes()).padStart(2, "0");
      const seconds = String(now.getSeconds()).padStart(2, "0");
      setTime(`${hours}:${minutes}:${seconds}`);
    };

    // 初始設置時間
    updateTime();

    // 設置定時器，每秒更新時間
    const timer = setInterval(updateTime, 1000);

    // 清除定時器
    return () => clearInterval(timer);
  }, []);

  return <div>現在時間：{time}</div>;
}

export default CurrentTime;