import React from 'react';
import PostItem from "./PersonItem";
import { TransitionGroup, CSSTransition } from "react-transition-group";

const PersonList = ({ persons, show, h2 }) => {

  if (!persons.length) {
    return (
      <h2 style={{ textAlign: 'center', padding: 50 }}>
        {h2}
      </h2>
    )
  }

  return (
    <div >
      <TransitionGroup>
        {persons.map((post, index) =>
          <CSSTransition
            key={index}
            timeout={500}
            classNames="post">
            <PostItem post={post} show={show} index={index + 1} />
          </CSSTransition>
        )}
      </TransitionGroup>
    </div>
  );
};

export default PersonList;
