import {useState} from "react"

function RestRegInfo() {
  const [info, setInfo] = useState([
    {id: 0, name : "銀魚", location : "小福", 
      mon : "11:00~19:00", tue : "11:00~19:00", wed : "11:00~19:00", 
      thu : "11:00~19:00", fri : "11:00~19:00", sat : "11:00~19:00", sun : ""},
    {id: 1, name : "大水缸", location : "科技大樓", 
      mon : "10:00~21:30", tue : "10:00~21:30", wed :"10:00~21:30", 
      thu : "10:00~21:30", fri : "10:00~21:30", sat : "10:00~21:30", sun : "10:00~21:30"},
  ])
  const days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"];

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