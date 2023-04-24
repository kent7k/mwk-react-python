import React, { useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { useNavigate } from 'react-router-dom'

import lodash_merge from 'lodash/merge'

import { userRegister } from '../../../store/actions'
import {
  clearGeo,
  clearSuccess,
} from '../../../store/slices/authentication/userSlice'
import { Page404 } from '../../pages/Page404'

import { RegisterFormStepFour } from './RegisterFormStepFour'
import { RegisterFormStepOne } from './RegisterFormStepOne'
import { RegisterFormStepThree } from './RegisterFormStepThree'
import { RegisterFormStepTwo } from './RegisterFormStepTwo'

export const Register = () => {
  const [step, setStep] = useState(1)
  const [formData, setFormData] = useState({})
  const dispatch: any = useDispatch()
  // TODO: Type RootState
  const { success } = useSelector((state: any) => state.user)

  const navigate = useNavigate()
  const lastStep = 4

  const handleSubmit = (data) => {
    dispatch(userRegister(data))
  }

  useEffect(() => {
    document.title = 'Registration || Website Title'
  }, [])

  useEffect(() => {
    if (success) {
      const successMessage =
        'You have successfully registered! To log in to your account, please check your email. You should have received an email with instructions on how to activate your account.'

      dispatch(clearSuccess())
      dispatch(clearGeo())

      navigate('/login/', {
        state: {
          message: successMessage,
        },
      })
    }
  }, [dispatch, success, navigate])

  const nextStep = (values) => {
    const formDataCopy = JSON.parse(JSON.stringify(formData))

    setFormData(lodash_merge(formDataCopy, values))

    if (step === lastStep) {
      handleSubmit(formDataCopy)
      return
    }

    setStep(step + 1)
  }

  const prevStep = () => {
    setStep(step - 1)
  }

  const generalRegisterProps = {
    values: formData,
    nextStep,
    prevStep,
  }

  const steps = {
    1: <RegisterFormStepOne title="APP" {...generalRegisterProps} />,
    2: (
      <RegisterFormStepTwo
        title="How should we address you?"
        {...generalRegisterProps}
      />
    ),
    3: (
      <RegisterFormStepThree
        title="Set up your profile"
        {...generalRegisterProps}
      />
    ),
    4: (
      <RegisterFormStepFour
        title="Choose a profile photo"
        {...generalRegisterProps}
      />
    ),
  }

  return steps[step] ? steps[step] : <Page404 />
}
