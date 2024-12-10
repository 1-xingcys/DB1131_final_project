import {useState, useEffect} from "react"
import { getRestRegInfo } from "../../api/restRegInfo";

import styles from "./custOther.module.css"; // 引入樣式模組

function RestRegInfo() {
  const [info, setInfo] = useState([]);
  const days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"];
  const dayNames = ["一", "二", "三", "四", "五", "六", "日"];

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await getRestRegInfo();
        setInfo(response);
        console.log("get restaurant regular info successful", response);
      } catch (error) {
        console.log("get restaurant regular info failed :", error.message);
      }
    };
  
    fetchData();
  }, []);
  

  return (
    <div className={styles.container}>
      {info.map((restaurant) => (
        <div key={restaurant.id} className={styles.card}>
          <div className={styles.cardHeader}>{restaurant.name}</div>
          <div className={styles.location}>📍{restaurant.location}</div>
          <ul className={styles.scheduleList}>
            {days.map((day, index) => (
              <li key={day} className={styles.scheduleItem}>
                <span className={styles.scheduleText}>
                  {dayNames[index]}：{restaurant[day] || "💤"}
                </span>
              </li>
            ))}
          </ul>
        </div>
      ))}
    </div>
  );
}

export default RestRegInfo;