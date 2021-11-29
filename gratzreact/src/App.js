import './styles/App.css';
import AppRouter from "./components/AppRouter";
import { useEffect, useState } from "react";
import { BrowserRouter } from "react-router-dom";
import { AppContext } from "./context";
import Navbar from "./components/ui/Navbar/Navbar";
import { themeColors } from './constants';

function App() {

  const [isAuth, setIsAuth] = useState(true);
  const [isLoading, setLoading] = useState(true);
  const [dayChosen, setDayChosen] = useState();
  const [langChosen, setLangChosen] = useState('ru');
  const [langCurrent, setLangCurrent] = useState('ru');
  const [themeIndex, setThemeIndex] = useState(0);

  useEffect(() => {
    if (themeIndex > 2) setThemeIndex(0)
    document.body.style.backgroundColor = themeColors[themeIndex]
  }, [themeIndex])



  return (
    <AppContext.Provider value={{
      isAuth, setIsAuth,
      dayChosen, setDayChosen,
      langChosen, setLangChosen,
      langCurrent, setLangCurrent,
      themeIndex, setThemeIndex,
      isLoading, setLoading
    }}>
      <BrowserRouter>
        <Navbar />
        <AppRouter />
      </BrowserRouter>
    </AppContext.Provider>
  )
}

export default App;
