import React from 'react';
import styles from "./placeOrder.module.css"

const ShoppingCart = ({ selectedRest, checkCart, shoppingCart, orderInfo, selectedDiscountRate }) => {
  if (!selectedRest || !checkCart) return null;

  const totalPrice = shoppingCart.reduce(
    (total, item) => total + item.price * item.quantity * (selectedDiscountRate ? selectedDiscountRate : 1),
    0
  );

  return (
    <div className={styles.cartContainer}>
      <p className={styles.cartTitle}>購物車</p>
      {shoppingCart.length > 0 ? (
        <ul className={styles.cartList}>
          {shoppingCart.map((item) => (
            <li className={styles.cartItem} key={item.name}>
              {item.name} x {item.quantity} = ${item.price * item.quantity}
            </li>
          ))}
        </ul>
      ) : (
        <p className={styles.info}>購物車是空的</p>
      )}
      <p className={styles.info}>需要餐具：{orderInfo.eating_utensil ? "是" : "否"}</p>
      <p className={styles.info}>需要塑膠袋：{orderInfo.plastic_bag ? "是" : "否"}</p>
      <p className={styles.info}>備註：{orderInfo.note || "無"}</p>
      <p className={styles.info}>{selectedDiscountRate ? `使用 ${selectedDiscountRate} 折價券` : `未使用折價券`}</p>
      <p className={styles.total}>總金額 = ${totalPrice}</p>
    </div>
  );
};

export default ShoppingCart;
