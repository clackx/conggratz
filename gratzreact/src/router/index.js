import SockPersons from "../pages/SockPersons";

export const privateRoutes = [
  { path: '/persons', component: <SockPersons />, exact: true },
  { path: '/persons/:bday', component: <SockPersons />, exact: true },
]

export const publicRoutes = []
