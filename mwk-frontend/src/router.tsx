import React from 'react'
import { BrowserRouter, Route, Routes } from 'react-router-dom'

import { Page404 } from './components/pages/Page404'

type RouteProps = {
  path: string
  component: React.ReactNode
  protection?: React.ReactNode
}

type RouterProps = {
  routes: RouteProps[]
}

export const Router: React.FC<RouterProps> = ({ routes }) => {
  const routeComponents = routes.map((route) => {
    if (!route.protection) {
      return (
        <Route key={route.path} path={route.path} element={route.component} />
      )
    }

    return (
      <Route key={route.path} element={route.protection}>
        <Route path={route.path} element={route.component} />
      </Route>
    )
  })

  return (
    <BrowserRouter>
      <Routes>
        {routeComponents}
        <Route path="*" element={<Page404 />} />
      </Routes>
    </BrowserRouter>
  )
}

export default Router
