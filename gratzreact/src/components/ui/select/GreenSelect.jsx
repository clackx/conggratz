import React from "react";
import cl from "./GreenSelect.module.css"
import Select, { components } from "react-select";
import { bgcolor, bgcolorsel, langDict, mediaURL } from "../../../constants";

const GreenSelect = ({ themeIndex, onChange }) => {

  var options = [];
  Object.keys(langDict).map((key) =>
    options.push({
      value: key,
      label: langDict[key],
      icon: mediaURL + "flag" + key + ".png",
    })
  );

  const selectStyles = {
    option: (base, state) => ({
      color: state.isSelected ? "#faa" : "",
      backgroundColor: state.isSelected ? bgcolorsel[themeIndex] : bgcolor[themeIndex],
      textAlign: "left",
      cursor: "pointer",
      "&:hover": {
        borderColor: "orange",
        backgroundColor: bgcolorsel[themeIndex],
        textShadow: "#074237 0px 1px",
      },
    }),
    container: (base) => ({
      ...base,
      backgroundColor: "transparent",
      width: "100%",
    }),
    menu: (base, state) => ({
      width: state.selectProps.width,
      color: state.selectProps.menuColor,
      backgroundColor: "transparent",
      marginTop: 20,
    }),
    menuList: (base) => ({
      ...base,
      "::-webkit-scrollbar": {
        width: "5px",
        height: "0px",
      },
      "::-webkit-scrollbar-track": {
        background: "orange",
      },
      "::-webkit-scrollbar-thumb": {
        background: "#2A2",
      },
      "::-webkit-scrollbar-thumb:hover": {
        background: "#F5F",
      },
    }),
    control: () => ({
      height: 32,
      minHeight: 32,
      cursor: "pointer",
    }),
    dropdownIndicator: (base) => ({
      ...base,
      display: "none",
    }),
    indicatorSeparator: (base) => ({
      ...base,
      display: "none",
    }),
    valueContainer: (base) => ({
      padding: 0,
      paddingLeft: 2,
    }),
  };

  const { Option } = components;
  const SingleOption = (props) => (
    <Option className={cl.mysingle} {...props}>
      <div className={cl.divopt1}>
        <img
          className={cl.flagimg1}
          src={props.data.icon}
          alt={props.data.label}
        />
        <div className={cl.textdiv}>{props.data.label}</div>
      </div>
    </Option>
  );

  const IconOption = (props) => (
    <Option className={cl.myoption} {...props}>
      <div className={cl.divopt2}>
        <img
          className={cl.flagimg2}
          src={props.data.icon}
          alt={props.data.label}
        />
        <div className={cl.textdiv}>{props.data.label}</div>
      </div>
    </Option>
  );

  return (
    <Select
      className={cl.myselect}
      defaultValue={options[0]}
      options={options}
      components={{ Option: IconOption, SingleValue: SingleOption }}
      isSearchable={false}
      styles={selectStyles}
      onChange={(selected) => onChange(selected.value)}
    />
  )
}

export default GreenSelect
