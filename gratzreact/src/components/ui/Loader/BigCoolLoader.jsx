import React from 'react';
import cl from './BigCoolLoader.module.css';

const BigCoolLoader = () => {
  return (
    <div className={cl.divloader}>
      <div className={cl.loader}>
      </div>
    </div>
  );
};

export default BigCoolLoader;
