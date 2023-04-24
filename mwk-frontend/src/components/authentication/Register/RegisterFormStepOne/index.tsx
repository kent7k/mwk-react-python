import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'

import Button from '@mui/material/Button'

import { useFormik } from 'formik'
import * as Yup from 'yup'

import { useLoad } from '../../../../hooks'
import { Form } from '../../Form'
import { FormFields } from '../../FormFields'

type RegisterFormStepOneProps = {
  values: {
    username?: string
    email?: string
    password?: string
    password2?: string
  }
  nextStep: (values: {
    username?: string
    email?: string
    password?: string
    password2?: string
  }) => void
  title: string
}

export const RegisterFormStepOne: React.FC<RegisterFormStepOneProps> = ({
  values: { username = '', email = '', password = '', password2 = '' },
  nextStep,
  title,
}) => {
  const [showErrors, setShowErrors] = useState(false)
  const isLoad = useLoad(200)
  const navigate = useNavigate()
  const validationSchema = Yup.object({
    username: Yup.string()
      .max(50, 'Username should not exceed 50 characters!')
      .min(4, 'Username should be at least 4 characters long.')
      .required('Please provide a username.'),
    email: Yup.string()
      .email('Please provide a valid email address!')
      .required('Please provide an email address.'),
    password: Yup.string()
      .min(8, 'Password should be at least 8 characters long.')
      .required('Please provide a password.'),
    password2: Yup.string()
      .required('Please provide password confirmation!')
      .oneOf([Yup.ref('password'), null], 'Passwords must match!'),
  })

  const formik = useFormik({
    initialValues: {
      username,
      email,
      password,
      password2,
    },
    validationSchema,
    onSubmit(values) {
      nextStep(values)
    },
  })

  const fields = [
    {
      name: 'username',
      type: 'text',
      label: 'Username',
    },
    {
      name: 'email',
      type: 'email',
      label: 'Email',
    },
    {
      name: 'password',
      type: 'password',
      label: 'Password',
    },
    {
      name: 'password2',
      type: 'password',
      label: 'Confirm Password',
    },
  ]

  const signInButton = (
    <Button
      type="button"
      size="large"
      fullWidth
      disabled={!isLoad}
      sx={{ mb: 2 }}
      onClick={() => {
        navigate('/login/')
      }}
      variant="contained"
    >
      Login
    </Button>
  )

  return (
    <Form
      title={title}
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
      buttons={{
        alterButton: signInButton,
      }}
      handleSubmit={formik.handleSubmit}
      setShowErrors={setShowErrors}
    />
  )
}
