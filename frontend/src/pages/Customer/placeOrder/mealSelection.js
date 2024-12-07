import React from 'react';
import styles from './placeOrder.module.css';

const MealSelection = ({ selectedRest, mealItemsForChosen, handleAddToCart }) => {
  if (!selectedRest) {
    return null;
  }

  return (
    <div className={styles.container}>
      
      <p className={styles.title}>請選擇您想要的餐點：</p>
      <ul className={styles.mealList}>
        {mealItemsForChosen.map((meal) => (
          <li key={meal.name} className={styles.mealItem}>
            <span>
              <span className={styles.mealName}>{meal.name}</span>
              <span className={styles.price}>${meal.price}</span>
            </span>
            <span>
              <input
                type="number"
                min="0"
                placeholder="數量"
                className={styles.input}
                onChange={(e) =>
                  handleAddToCart(meal, parseInt(e.target.value, 10) || 0)
                }
              />
              <span className={styles.processingTime}>
                （製作時間約 {meal.processing_time} 分鐘）
              </span>
              <span className={styles.processingTime}>剩餘 {meal.supply_num} 份</span>
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default MealSelection;
