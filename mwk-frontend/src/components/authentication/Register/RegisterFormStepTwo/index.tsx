import React, { useState } from 'react'

import { useFormik } from 'formik'
import * as Yup from 'yup'

import { Form } from '../../Form'
import { FormFields } from '../../FormFields'

interface Props {
  title: string
  values: {
    first_name?: string
    last_name?: string
  }
  prevStep: () => void
  nextStep: (values: { first_name?: string; last_name?: string }) => void
}

export const RegisterFormStepTwo: React.FC<Props> = ({
  title,
  values,
  prevStep,
  nextStep,
}) => {
  const [showErrors, setShowErrors] = useState(false)
  const validationSchema = Yup.object({
    firstName: Yup.string()
      .max(30, 'First name should not exceed 30 characters!')
      .required('Please provide a first name.'),
    lastName: Yup.string()
      .max(30, 'Last name should not exceed 30 characters!')
      .required('Please provide a last name.'),
  })

  const { first_name = '', last_name = '' } = values

  const formik = useFormik({
    initialValues: {
      first_name,
      last_name,
    },
    validationSchema,
    onSubmit() {
      nextStep(values)
    },
  })

  const fields = [
    {
      name: 'firstName',
      type: 'text',
      label: 'first name',
    },
    {
      name: 'lastName',
      type: 'text',
      label: 'last name',
    },
  ]

  return (
    <Form
      handleSubmit={formik.handleSubmit}
      setShowErrors={setShowErrors}
      buttons={{ prevButton: { prevStep } }}
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
