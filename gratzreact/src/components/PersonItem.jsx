import React, { useContext } from "react";
import { AppContext } from "../context";
import "../styles/Card.css"

const PersonItem = (props) => {

  const { langCurrent } = useContext(AppContext)

  const getJoined = (list) => {
    if (['zh', 'ja', 'ko'].includes(langCurrent)) {
      return list.map(x => x[1][langCurrent]).join('、')
    } else {
      return (<i> {list.map(x => x[1][langCurrent]).join(', ')} </i>)
    }
  }

  return (
    <div onClick={() => props.show(props.post)} className="card">
      <div className="container">
        <p className="personname">{props.post.links[langCurrent]}</p>
        <p className="persondescr">{props.post.descrs[langCurrent]}</p>
        <div style={{ marginTop: 10 }}>
          <p className="personoccus">
            {getJoined(props.post.occupations.list)}
          </p>
        </div>
      </div>

      <div >
        <img
          className="personphoto"
          src={props.post.photo}
          alt="" />
      </div>
    </div>
  );
};

export default PersonItem;
