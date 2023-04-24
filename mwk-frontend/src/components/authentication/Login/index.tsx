import React, { useEffect, useState } from 'react'
import { useDispatch } from 'react-redux'
import { useLocation } from 'react-router-dom'

import { userLogin } from '../../../store/actions'

import { LoginForm } from './LoginForm'

export const Login = () => {
  const locationContext = useLocation()
  const [message, setMessage] = useState(
    locationContext.state ? 'locationContext.state.message' : ''
  )
  const dispatch: any = useDispatch()

  const handleSubmit = (data) => {
    dispatch(userLogin(data))
  }

  useEffect(() => {
    document.title = 'Login || Website Title'
  }, [])

  return (
    <LoginForm
      title="Login"
      message={message}
      setMessage={setMessage}
      submit={handleSubmit}
    />
  )
}
