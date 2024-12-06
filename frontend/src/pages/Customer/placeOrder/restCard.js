import React from 'react';
import styles from './placeOrder.module.css';

const RestaurantCards = ({ selectedRest, handleRestSelect, restNames }) => {
  if(selectedRest) return null;
  return (
    <div>
      <h1>選擇餐廳</h1>
      <div className={styles.cardsContainer}>
        {restNames.map((restaurant) => (
          <div
            key={restaurant.id}
            className={`${styles.card} ${
              selectedRest === restaurant.id ? styles.cardSelected : ''
            }`}
            onClick={() => handleRestSelect(restaurant.id)}
          >
            <div className={styles.cardName}>{restaurant.name}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RestaurantCards;
