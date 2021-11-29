export const getDate = (dayChosen, offset) => {
  const mdate = new Date();
  if (dayChosen) {
    mdate.setMonth(parseInt(dayChosen.slice(0, 2)) - 1);
    mdate.setDate(parseInt(dayChosen.slice(-2)) + offset);
  }
  return mdate;
};

export const getLongDate = (dayChosen, langCurrent) => {
  var options = { month: "long", day: "numeric" };
  return getDate(dayChosen, 0).toLocaleDateString(langCurrent, options);
};

export const getShortDate = (dayChosen, langCurrent, offset) => {
  var options = { month: "short", day: "numeric" };
  return getDate(dayChosen, offset).toLocaleDateString(langCurrent, options);
};

export const getDigitsDate = (dayChosen, offset) => {
  const ddate = getDate(dayChosen, offset);
  return (
    ("0" + (ddate.getMonth() + 1)).slice(-2) + "." +
    ("0" + ddate.getDate()).slice(-2)
  );
};
