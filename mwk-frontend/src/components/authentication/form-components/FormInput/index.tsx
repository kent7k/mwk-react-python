import React from 'react'

import TextField from '@mui/material/TextField'

import { FormAvatarUploader as Avatar } from '../FormAvatarUploader'
import { FormDatePicker as DatePicker } from '../FormDatePicker'
import { FormSelect as Select } from '../FormSelect'

type DateType = Date | null

type FormInputProps = {
  element: {
    type: 'text' | 'password' | 'email' | 'date' | 'select' | 'avatar'
    label: string
    name: string
    options: { value: any; label: string }[]
    getLabel?: (option: any) => string
    filterOptions?: (options: any[], filter: string) => any[]
    render?: (option: any) => React.ReactNode
    disabled?: boolean
    compareFunc?: (option: any, value: any) => boolean
    loading: boolean
    minDate?: Date
    maxDate?: Date
    width: number
    height: number
    id: string
  }
  value: DateType
  setValue: any
  errors: any
  touched: any
  handleChange: any
  handleBlur: (e: React.FocusEvent<HTMLInputElement>) => void
  handleKeyDown: (e: React.KeyboardEvent<HTMLInputElement>) => void
  setError: (fieldName: string, errorMessage: string | undefined) => void
  showErrors: boolean
}

export const FormInput: React.FC<FormInputProps> = ({
  element,
  value,
  errors,
  touched,
  handleChange,
  handleBlur,
  handleKeyDown,
  setError,
  showErrors,
}) => {
  const showError = (isTouched, isErrors) => {
    if (isTouched && isErrors) {
      return true
    }
    return false
  }

  const showErrorText = (isTouched, isErrors, show) => {
    if (isTouched && isErrors && show) {
      return errors[element.name]
    }
    return ''
  }

  const generalTextFieldProps = {
    fullWidth: true,
    error: showError(touched[element.name], errors[element.name]),
    helperText: showErrorText(
      touched[element.name],
      errors[element.name],
      showErrors
    ),
    FormHelperTextProps: { sx: { marginLeft: 0 } },
    onBlur: handleBlur,
    id: element.name,
    name: element.name,
  }

  const getTextInput = () => (
    <TextField
      type={element.type}
      label={element.label}
      value={value}
      onChange={handleChange}
      {...generalTextFieldProps}
      inputProps={{
        onKeyDown: handleKeyDown,
      }}
    />
  )

  const getPicker = () => (
    <DatePicker
      value={value}
      label={element.label}
      onChange={handleChange}
      minDate={element.minDate}
      maxDate={element.maxDate}
      textFieldProps={generalTextFieldProps}
    />
  )

  const getSelect = () => (
    <Select
      loading={element.loading}
      textFieldProps={generalTextFieldProps}
      options={element.options}
      getOptionLabel={element.getLabel}
      label={element.label}
      filterOptions={element.filterOptions}
      render={element.render}
      disabled={element.disabled}
      compareFunc={element.compareFunc}
      handleChange={handleChange}
      valueProps={value}
    />
  )

  const getAvatar = () => (
    <Avatar
      width={element.width}
      height={element.height}
      name={element.name}
      setError={setError}
      helperText={showErrorText(
        touched[element.name],
        errors[element.name],
        showErrors
      )}
      handleChange={handleChange}
      // value={value}
      id={element.id}
      // label={element.label}
    />
  )

  const inputTypes = {
    text: getTextInput(),
    password: getTextInput(),
    email: getTextInput(),
    date: getPicker(),
    select: getSelect(),
    avatar: getAvatar(),
  }

  return inputTypes[element.type]
}
