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
    {eating_utensil : false, plastic_bag : false, note : "", coupon_id: null}
  );
  const [checkCart, setCheckCart] = useState(false);

  const [selectedDiscountRate, setSelectedDiscountRate] = useState("");
  const [couponId, setCouponId] = useState(null); // 用於存儲驗證成功的 coupon_id

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await getRestName();
        setrestName(response);
        console.log("get restaurant names successful", response);
      } catch (error) {
        console.log("get restaurant names failed :", error.error);
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
    setOrderInfo({eating_utensil : false, plastic_bag : false, note : "", coupon_id: null});
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

  const handleSubmit = async () => {
    const order_processing_time = shoppingCart.reduce((total, item) => {return total += item.processing_time * item.quantity}, 0);
    const mealItems = shoppingCart.map((item) => ({name : item.name, number : item.quantity }));

    console.log(shoppingCart.map((item) => (
       `${item.name} : ${item.quantity} = $${item.price * item.quantity}`
    )));
    console.log(`需要餐具：${orderInfo.eating_utensil ? "是" : "否"}`,
      `需要塑膠袋：${orderInfo.plastic_bag ? "是" : "否"}`,
      `備註：${orderInfo.note || "無"}`)
    console.log(`折價券編號：${orderInfo.coupon_id || "無"}`);
    console.log(`折扣率為 ${selectedDiscountRate}`);
    console.log(`預計備餐時間 ＝ ${order_processing_time}`);
    console.log(`總金額 = $${shoppingCart.reduce((total, item) => {return total += item.price * item.quantity}, 0)}`)
    
    try {
      const response = await submitOrder(order_processing_time, orderInfo.eating_utensil, 
        orderInfo.plastic_bag, orderInfo.note, 
        sessionStorage.getItem("username"), selectedRest, mealItems, orderInfo.coupon_id);
      console.log(`submitOrder response : ${response}`);
      if(response.getCoupon){
        alert(`訂單已送出！\n獲得 ${response.discount_rate} 折價券！
          使用期限為 ${new Date(response.start_date).toISOString().split("T")[0]} ~ ${new Date(response.due_date).toISOString().split("T")[0]}`);
      } else alert("訂單已送出！");
      resetOrder();
    } catch(error) {
      resetOrder();
      alert(error);
    }
  }

  const resetOrder = () => {
    setShoppingCart([]);
    setOrderInfo({eating_utensil : false, plastic_bag : false, note : "",coupon_id: null});
    setSelectedRest("");
    setSelectedDiscountRate("");
    setCouponId("");
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
        <OrderDetailsForm 
          orderInfo={orderInfo} 
          onOrderInfoChange={handleOrderInfoChange}
          couponId={couponId}
          setCouponId={setCouponId}
          selectedDiscountRate={selectedDiscountRate}
          setSelectedDiscountRate={setSelectedDiscountRate} />
      </div>}
      
      <div>
        <ShoppingCart
          selectedRest={selectedRest}
          checkCart={checkCart}
          shoppingCart={shoppingCart}
          orderInfo={orderInfo}
          selectedDiscountRate={selectedDiscountRate}
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

