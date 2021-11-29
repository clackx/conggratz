import React from "react";
import cl from './DateButton.module.css'

const DateButton = ({ text }) => {
  return (
    <button className={cl.button29}>
      <p className={cl.buttp}>{text}</p>
    </button>
  )
}

export default DateButton
