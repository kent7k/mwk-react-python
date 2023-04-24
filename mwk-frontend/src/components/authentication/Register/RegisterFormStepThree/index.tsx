import React, { useState } from 'react'

import { useFormik } from 'formik'
import moment from 'moment'
import * as Yup from 'yup'

import { Form } from '../../Form'
import { FormFields } from '../../FormFields'

type RegisterFormStepThreeProps = {
  values: {
    profile?: {
      birthday?: Date | null
    }
  }
  nextStep: (values: {
    profile: { birthday?: string; }
  }) => void
  prevStep: () => void
  title: string
}

export const RegisterFormStepThree: React.FC<RegisterFormStepThreeProps> = ({
  values,
  nextStep,
  prevStep,
  title,
}) => {
  const [showErrors, setShowErrors] = useState(false)

  const {
    birthday = null,
  } = values.profile ? values.profile : {}

  const validationSchema = Yup.object({
    birthdaySchema: Yup.date()
      .typeError('Please enter a valid date of birth!')
      .required('Please provide a date of birth!')
      .test({
        name: 'is_older_than_fourteen',
        test(value, fail) {
          if (!value) {
            return false
          }
          const birthdaySchema = value.toJSON().slice(0, 10).split('-').join('')

          const yearsOld = moment().diff(
            moment(birthdaySchema, 'YYYYMMDD'),
            'years'
          )

          if (yearsOld < 14) {
            return fail.createError({
              message: 'You must be at least 14 years old!',
            })
          }

          return true
        },
      }),
  })

  const formik = useFormik({
    initialValues: {
      birthday,
    },
    validationSchema,
    onSubmit(e) {
      const getFormatDate = (date) => {
        // parse YYYY-mm-dd
        if (date.length === 10) {
          // Already YYYY-mm-dd
          return date
        }
        return e.birthday?.toJSON().slice(0, 10)
      }

      const JSONValues = {
        ...JSON.parse(JSON.stringify(values)),
        birthday: getFormatDate(e.birthday),
      }

      nextStep({
        profile: JSONValues,
      })
    },
  })

  const fields = [
    {
      name: 'birthday',
      type: 'date',
      label: 'Birthday',

      handleChange() {
        const setValue = (val) => {
          // eslint-disable-next-line react/no-this-in-sfc
          formik.setFieldTouched(this.name, true)
          // eslint-disable-next-line react/no-this-in-sfc
          formik.setFieldValue(this.name, val, true)
        }
        return setValue
      },
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
          setValue={formik.setFieldValue}
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
