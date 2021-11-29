import React from "react";
import cl from './PicButton.module.css'

const MyButton = ({children}) => {
    return (
        <button className={cl.button28}>
            {children}
        </button>
    )
}

export default MyButton
