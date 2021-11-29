import { useContext } from "react";
import { Route, Routes, Navigate } from "react-router-dom";
import { AppContext } from "../context";
import { privateRoutes, publicRoutes } from "../router";

const AppRouter = () => {
  const { isAuth } = useContext(AppContext)
  return (
    isAuth
      ? <Routes>
        {privateRoutes.map(route =>
          <Route
            element={route.component}
            path={route.path}
            exact={route.exact}
            key={route.path} />)}
        <Route path="/" element={<Navigate replace to="/persons" />} />
      </Routes>
      : <Routes>
        {publicRoutes.map(route =>
          <Route
            element={route.component}
            path={route.path}
            exact={route.exact}
            key={route.path} />)}
        <Route path="/" element={<Navigate replace to="/login" />} />
      </Routes>

  )
}

export default AppRouter;
