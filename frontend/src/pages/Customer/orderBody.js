import {useState} from "react"
import OrderDetailsForm from "./orderNoteForm";

function OrderForm(){
  const [info, setInfo] = useState([
    {id: 0, name : "銀魚", 
      meal : [
        {name: "椒麻雞", price: 100},
        {name: "咖哩雞", price: 100}
        ]
    },
    {id: 1, name : "大水缸",
      meal : [
        {name: "鍋燒意麵", price: 100},
        {name: "泡菜意麵", price: 120},
        {name: "滷味個人餐", price: 50}
        ]
    }
  ]);
  const [shoppingCart, setShoppingCart] = useState([]);
  const [selectedRest, setSelectedRest] = useState("");
  const [orderInfo, setOrderInfo] = useState(
    {eating_utensil : false, plastic_bag : false, note : ""}
  );
  const [checkCart, setCheckCart] = useState(false);

  // 更新購物車
  const handleAddToCart = (meal, quantity) => {
    setShoppingCart((prevCart) => {
      const existingItem = prevCart.find((item) => item.name === meal.name);
      if (existingItem) {
        // 更新已存在餐點
        if (quantity)
          return prevCart.map((item) =>
            item.name === meal.name
              ? { ...item, quantity: quantity }
              : item
          );
        return prevCart.filter((item) => item.name !== meal.name);
      } else {
        // 添加新餐點到購物車
        return quantity ? [...prevCart, { ...meal, quantity }] : prevCart;
      }
    });
  };

  const handleRestSelect = (e) => {
    setSelectedRest(e.target.value);
  }

  const handleOrderInfoChange = (updatedInfo) => {
    setOrderInfo(updatedInfo); // 更新訂單資訊
  };

  const handleCheckCart = () => {
    setCheckCart(!checkCart);
  }


  // 使用者要訂的那間餐廳
  const selectedRestaurant = info.find(
    (rest) => rest.name === selectedRest
  );

  const handleSubmit = () => {
    console.log(shoppingCart.map((item) => (
       `${item.name} : ${item.quantity} = $${item.price * item.quantity}`
    )))
    console.log(`需要餐具：${orderInfo.eating_utensil ? "是" : "否"}`,
      `需要塑膠袋：${orderInfo.plastic_bag ? "是" : "否"}`,
      `備註：${orderInfo.note || "無"}`)

    console.log(`總金額 = $${shoppingCart.reduce((total, item) => {return total += item.price * item.quantity}, 0)}`)

    setShoppingCart([]);
    setOrderInfo([]);
    setSelectedRest("");
  }


  return (
    <div>
      <h2>點餐區</h2>

      {/* 下拉選單選擇餐廳 */}

      <div>
      <label htmlFor="order-rest-select">選擇餐廳：</label>
      <select id="order-rest-select" value={selectedRest} onChange={handleRestSelect}>
        <option value="">-- 請選擇餐廳 --</option>
        {info.map((restaurant) => (
          <option key={restaurant.id} value={restaurant.name}>
            {restaurant.name}
          </option>
        ))}
      </select>
      </div>

      {/* 選擇餐點 */}
      {selectedRest && <div>
        <p>請選擇您想要的餐點：</p>
        <ul>
          {selectedRestaurant.meal.map((meal) => (
            <li key={meal.name}>
              {meal.name} - ${meal.price}
              <input
                type="number"
                min="0"
                placeholder="數量"
                onChange={(e) =>
                  handleAddToCart(meal, parseInt(e.target.value, 10) || 0)
                }
              />
            </li>
          ))}
        </ul>
        {/* 處理餐具、塑膠袋、備註 */}
        <OrderDetailsForm orderInfo={orderInfo} onOrderInfoChange={handleOrderInfoChange} />

        {/* 是否顯示購物車按鈕 */}
        <button onClick={handleCheckCart}>{checkCart ? "隱藏購物車" : "查看購物車"}</button>  
      </div>}



      {/* 顯示購物車 */}
      {selectedRest && checkCart && <div>
        <h2>購物車</h2>
        {shoppingCart.length > 0 ? (
          <ul>
            {shoppingCart.map((item) => (
              <li key={item.name}>
                {item.name} x {item.quantity} = ${item.price * item.quantity}
              </li>
            ))}
          </ul>
        ) : (
          <p>購物車是空的</p>
        )}
        
        <div>
          <p>需要餐具：{orderInfo.eating_utensil ? "是" : "否"}</p>
          <p>需要塑膠袋：{orderInfo.plastic_bag ? "是" : "否"}</p>
          <p>備註：{orderInfo.note || "無"}</p>
        </div>

        <p>總金額 = ${shoppingCart.reduce((total, item) => {return total += item.price * item.quantity}, 0)}</p>
      </div>}

      {selectedRest && (<button onClick={handleSubmit}>提交訂單</button>)}


    </div>
  );
}

export default OrderForm;