import React, { useEffect } from 'react'
import { Outlet, useNavigate } from 'react-router-dom'

import { useUser } from '../../../hooks/useUser'

export const AnonymousProtectedRoute = () => {
  const [token] = useUser()
  const navigate = useNavigate()

  useEffect(() => {
    if (token) {
      navigate('/feed/')
    }
  }, [navigate, token])

  if (token) {
    return null
  }

  // returns child route elements
  return <Outlet />
}
export default AnonymousProtectedRoute
