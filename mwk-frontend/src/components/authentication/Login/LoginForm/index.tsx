import React, { useState } from 'react'
import { useSelector } from 'react-redux'
import { useNavigate } from 'react-router-dom'

import Button from '@mui/material/Button'

import { useFormik } from 'formik'
import * as Yup from 'yup'

import { useLoad } from '../../../../hooks/useLoad'
import { Form } from '../../Form'
import { FormFields } from '../../FormFields'

interface LoginFormProps {
  submit: (values: { username: string; password: string }) => void
  message: string
  setMessage: (message: string) => void
  title: string
}

export const LoginForm: React.FC<LoginFormProps> = ({
  submit,
  message,
  setMessage,
  title,
}) => {
  const [showErrors, setShowErrors] = useState(false)
  const navigate = useNavigate()
  const isLoad = useLoad(200)
  // TODO: Type RootState
  const { loading } = useSelector((state: any) => state.user)

  const validationSchema = Yup.object({
    username: Yup.string()
      .max(50, 'Username should not be longer than 50 characters!')
      .min(4, 'Username should be at least 4 characters long.')
      .required('Please provide a username!'),

    password: Yup.string()
      .min(8, 'Password should be longer than 8 characters')
      .required('Please provide a password!'),
  })

  const formik = useFormik({
    initialValues: {
      username: '',
      password: '',
    },
    validationSchema,
    onSubmit(values) {
      submit(values)
    },
  })

  const fields = [
    {
      name: 'username',
      type: 'text',
      label: 'Login',
    },
    {
      name: 'password',
      type: 'password',
      label: 'Password',
    },
  ]

  const signUpButton = (
    <Button
      type="button"
      size="large"
      fullWidth
      disabled={!isLoad}
      sx={{ mb: 2 }}
      onClick={() => {
        navigate('/')
      }}
      variant="contained"
    >
      Registration
    </Button>
  )

  return (
    <Form
      handleSubmit={formik.handleSubmit}
      setShowErrors={setShowErrors}
      buttons={{
        alterButton: signUpButton,
        loading,
      }}
      message={message}
      setMessage={setMessage}
      fields={
        <FormFields
          fields={fields}
          showErrors={showErrors}
          handleChange={formik.handleChange}
          handleBlur={formik.handleBlur}
          touched={formik.touched}
          errors={formik.errors}
          values={formik.values}
        />
      }
      title={title}
    />
  )
}
