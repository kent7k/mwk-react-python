import React, { useState } from 'react'
import { useSelector } from 'react-redux'

import { useFormik } from 'formik'
import * as Yup from 'yup'

import { Form } from '../../Form'
import { FormFields } from '../../FormFields'

type Props = {
  values: {
    avatar?: string
  }
  title: string
  nextStep: (data: { profile: { avatar?: string } }) => void
  prevStep: () => void
}

export const RegisterFormStepFour: React.FC<Props> = ({
  values: { avatar: defaultAvatar = '' },
  title,
  nextStep,
  prevStep,
}) => {
  const [showErrors, setShowErrors] = useState(false)
  const isFetching = useSelector((state: any) => state.user.loading)

  const validationSchema = Yup.object({
    avatar: Yup.array().nullable(),
  })

  const formik = useFormik({
    initialValues: { avatar: defaultAvatar },
    validationSchema,
    onSubmit: ({ avatar }) => {
      nextStep({ profile: { avatar } })
    },
  })

  const fields = [
    {
      name: 'avatar',
      type: 'avatar',
      label: 'Profile photo',
      width: 100,
      height: 100,

      handleChange() {
        const setValue = (val, shouldValidate = true) => {
          // eslint-disable-next-line react/no-this-in-sfc
          formik.setFieldTouched(this.name, true, shouldValidate)
          // eslint-disable-next-line react/no-this-in-sfc
          formik.setFieldValue(this.name, val, shouldValidate)
        }
        return setValue
      },
    },
  ]

  return (
    <Form
      handleSubmit={() => {
        if (formik.isValid) {
          formik.handleSubmit()
        }
      }}
      setShowErrors={setShowErrors}
      buttons={{
        prevButton: { prevStep },
        loading: isFetching,
      }}
      fields={
        <FormFields
          fields={fields}
          setValue={formik.setFieldValue}
          showErrors={showErrors}
          handleChange={formik.handleChange}
          setFieldError={formik.setFieldError}
          touched={formik.touched}
          errors={formik.errors}
          values={formik.values}
        />
      }
      title={title}
    />
  )
}
