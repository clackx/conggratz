import React, { useContext, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { AppContext } from "../../../context";
import { langList, mediaURL, themeList, titleL11ns } from "../../../constants";
import { getDigitsDate, getLongDate, getShortDate } from "../../../misc/dates";
import GreenSelect from "../select/GreenSelect";
import DateButton from "../button/DateButton";
import PicButton from "../button/PicButton";
import DottedLoader from "../Loader/DottedLoader";
import cl from './Navbar.module.css';

const Navbar = () => {
  const {
    langCurrent, setLangCurrent,
    dayChosen, setLangChosen,
    themeIndex, setThemeIndex,
    isLoading
  } = useContext(AppContext);
  const [themeName, setThemeName] = useState('dusk');
  const [langIndex, setLangIndex] = useState(0);

  const getLocalizedTitle = () => {
    return (
      <div>
        {getLongDate(dayChosen, langCurrent)}<br />
        {titleL11ns[langCurrent]}
      </div>
    );
  };

  useEffect(() => {
    setThemeName(themeList[themeIndex])
  }, [themeIndex]);

  useEffect(() => {
    setLangCurrent(langList[langIndex]);
    if (langIndex > 11) setLangIndex(0);
  }, [langIndex, setLangCurrent]);

  return (
    <div className={cl.headcontainer}>
      <div className={cl.left}
        style={{ backgroundImage: "url(" + mediaURL + "left_" + themeName + ".png)" }}>
        <GreenSelect onChange={setLangChosen} themeIndex={themeIndex} />
      </div>
      <div className={cl.center}>
        <div className={cl.centeredge}>
          <Link className="lnk" to={"/persons/" + getDigitsDate(dayChosen, -1)}>
            <DateButton text={getShortDate(dayChosen, langCurrent, -1)} />
          </Link>
        </div>

        <div className={cl.centercenter}>
          <h2>{getLocalizedTitle()}</h2>
          {isLoading &&
            <DottedLoader />}
        </div>

        <div className={cl.centeredge}>
          <Link className="lnk" to={"/persons/" + getDigitsDate(dayChosen, +1)}>
            <DateButton text={getShortDate(dayChosen, langCurrent, 1)} />
          </Link>
        </div>
      </div>
      <div
        className={cl.right}
        style={{ backgroundImage: "url(" + mediaURL + "right_" + themeName + ".png)" }}>
        <div className={cl.rightdiv}>
          <PicButton>
            <img
              className={cl.buttonimg}
              src={mediaURL + themeName + ".png"}
              alt={themeName}
              onClick={() => setThemeIndex(themeIndex + 1)}
            />
          </PicButton>

          <PicButton>
            <img
              className={cl.buttonimg}
              src={mediaURL + "flag" + langCurrent + ".png"}
              alt={langCurrent}
              onClick={() => setLangIndex(langIndex + 1)}
            />
          </PicButton>
        </div>
      </div>
    </div>
  );
};

export default Navbar;
