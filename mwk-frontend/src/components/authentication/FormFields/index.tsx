import React from 'react'

import { handleEnter } from '../../../lib/authentication'
import { FormInput as Input } from '../form-components/FormInput'

export function FormFields(props) {
  const getValue = (element) => {
    if ('value' in element) {
      return element.value
    }
    return props.values[element.name]
  }

  const getHandleChange = (element) => {
    if ('handleChange' in element) {
      return element.handleChange()
    }
    return props.handleChange
  }

  return props.fields.map((element) => (
    <Input
      key={element.name}
      showErrors={props.showErrors}
      element={element}
      handleChange={getHandleChange(element)}
      handleBlur={props.handleBlur}
      handleKeyDown={handleEnter}
      setError={props.setFieldError}
      touched={props.touched}
      errors={props.errors}
      setValue={props.setValue}
      value={getValue(element)}
    />
  ))
}
