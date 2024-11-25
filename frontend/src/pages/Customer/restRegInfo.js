import {useState, useEffect} from "react"
import { getRestRegInfo } from "../../api/restRegInfo";

function RestRegInfo() {
  const [info, setInfo] = useState([]);
  const days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"];

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
    <div>
      <h1>所有商家資訊</h1>
      
      {/* 動態呈現餐廳資訊 */}
      <div>
        {info.map((restaurant) => (
          <div key={restaurant.id} style={{ marginBottom: "20px" }}>
            <h2>{restaurant.name}</h2>
            <p>地點: {restaurant.location}</p>

            {/* 顯示營業時間 */}
            <h3>營業時間：</h3>
            <ul>
              {days.map((day) => (
                <li key={day}>
                  {day.charAt(0).toUpperCase() + day.slice(1)}:{" "}
                  {restaurant[day] || "休息日"}
                  {/* A || B  iff 
                  if (A == true) return A; else return B; */}
                </li>
              ))}
            </ul>
          </div>
        ))}
      </div>
    </div>
  );
}

export default RestRegInfo;