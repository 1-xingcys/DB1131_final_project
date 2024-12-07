import {useEffect, useState} from "react"
import OrderDetailsForm from "./orderNoteForm";
import { getRestName } from "../../../api/restNames";
import { getRestAvailableMealItem } from "../../../api/restMealItem";
import { submitOrder } from "../../../api/submitOrder";
import RestaurantCards from "./restCard";
import MealSelection from "./mealSelection";
import ShoppingCart from "./ShoppingCart";

import styles from "./placeOrder.module.css"

function OrderForm(){
  const [restNames, setrestName] = useState([]);
  const [mealItemsForChosen, setMealItemsForChosen] = useState([]);

  const [shoppingCart, setShoppingCart] = useState([]);
  const [selectedRest, setSelectedRest] = useState("");
  const [orderInfo, setOrderInfo] = useState(
    {eating_utensil : false, plastic_bag : false, note : ""}
  );
  const [checkCart, setCheckCart] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await getRestName();
        setrestName(response);
        console.log("get restaurant names successful", response);
      } catch (error) {
        console.log("get restaurant names failed :", error.message);
      }
    };

    fetchData();
    }, []);

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

  const handleRestSelect = (id) => {
    setShoppingCart([]);
    setOrderInfo({eating_utensil : false, plastic_bag : false, note : ""});
    setSelectedRest(id);
    console.log("select restaurant is : ", id);
    updateMealItems(id);
  }

  const handleOrderInfoChange = (updatedInfo) => {
    setOrderInfo(updatedInfo); // 更新訂單資訊
  };

  const handleCheckCart = () => {
    setCheckCart(!checkCart);
  }

  const updateMealItems = async (r_id) => {
    try {
      const response = await getRestAvailableMealItem(r_id);
      setMealItemsForChosen(response);
      console.log("update meal items successful", response);
    } catch(error) {
      console.log("update meal item fail: ", error.message);
    }
  };

  const handleSubmit = () => {
    const order_processing_time = shoppingCart.reduce((total, item) => {return total += item.processing_time * item.quantity}, 0);
    const mealItems = shoppingCart.map((item) => ({name : item.name, number : item.quantity }));

    console.log(shoppingCart.map((item) => (
       `${item.name} : ${item.quantity} = $${item.price * item.quantity}`
    )));
    console.log(`需要餐具：${orderInfo.eating_utensil ? "是" : "否"}`,
      `需要塑膠袋：${orderInfo.plastic_bag ? "是" : "否"}`,
      `備註：${orderInfo.note || "無"}`)
    console.log(`預計備餐時間 ＝ ${order_processing_time}`);
    console.log(`總金額 = $${shoppingCart.reduce((total, item) => {return total += item.price * item.quantity}, 0)}`)

    try {
      submitOrder(order_processing_time, orderInfo.eating_utensil, 
        orderInfo.plastic_bag, orderInfo.note, 
        sessionStorage.getItem("username"), selectedRest, mealItems);
      alert("訂單已送出！")
    } catch(error) {
      throw error;
    }

    resetOrder();
  }

  const resetOrder = () => {
    setShoppingCart([]);
    setOrderInfo({eating_utensil : false, plastic_bag : false, note : ""});
    setSelectedRest("");
  }


  return (
    <div>
      <div>
        <RestaurantCards
          selectedRest={selectedRest}
          handleRestSelect={handleRestSelect}
          restNames={restNames}
        />
      </div>

      <div>
        <MealSelection
          selectedRest={selectedRest}
          mealItemsForChosen={mealItemsForChosen}
          handleAddToCart={handleAddToCart}
        />
      </div>

      {/* 選擇餐點 */}
      {selectedRest && <div>
        {/* 處理餐具、塑膠袋、備註 */}
        <OrderDetailsForm orderInfo={orderInfo} onOrderInfoChange={handleOrderInfoChange} />
      </div>}
      
      <div>
        <ShoppingCart
          selectedRest={selectedRest}
          checkCart={checkCart}
          shoppingCart={shoppingCart}
          orderInfo={orderInfo}
        />
      </div>
      {/* 是否顯示購物車按鈕 */}

      {selectedRest && <div className={styles.cardsContainer}>
        <button className={styles.card} onClick={resetOrder}>返回</button>
        <button className={styles.card} onClick={handleCheckCart}>{checkCart ? "隱藏購物車" : "查看購物車"}</button>
        <button className={styles.card} onClick={handleSubmit}>提交訂單</button>
      </div>}
      

    </div>
  );
}

export default OrderForm;