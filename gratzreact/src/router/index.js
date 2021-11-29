import Persons from "../pages/Persons";

export const privateRoutes = [
  { path: '/persons', component: <Persons />, exact: true },
  { path: '/persons/:bday', component: <Persons />, exact: true },
]

export const publicRoutes = []
