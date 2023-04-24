import React from 'react'

import TextField, { TextFieldProps } from '@mui/material/TextField'
import useMediaQuery from '@mui/material/useMediaQuery'
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns'
import { DesktopDatePicker } from '@mui/x-date-pickers/DesktopDatePicker'
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider'
import { MobileDatePicker } from '@mui/x-date-pickers/MobileDatePicker'

import ruLocale from 'date-fns/locale/ru'

type DateType = Date | null

interface FormDatePickerProps {
  label?: string
  value: DateType
  onChange: any
  minDate?: DateType
  maxDate?: DateType
  textFieldProps?: TextFieldProps
  handleChange?: any
}

export const FormDatePicker: React.FC<FormDatePickerProps> = ({
  label,
  value,
  onChange,
  minDate,
  maxDate,
  textFieldProps,
}) => {
  const isMobile = useMediaQuery('(max-width:576px)')

  const pickerProps = {
    label,
    inputFormat: 'dd/MM/yyyy',
    value,
    onChange,
    minDate,
    maxDate,
    renderInput: (params) => <TextField {...params} {...textFieldProps} />,
  }

  const getPicker = () => {
    const mobilePicker = <MobileDatePicker {...pickerProps} />
    const desktopPicker = <DesktopDatePicker {...pickerProps} />

    if (isMobile) {
      return mobilePicker
    }
    return desktopPicker
  }
  return (
    <LocalizationProvider adapterLocale={ruLocale} dateAdapter={AdapterDateFns}>
      {getPicker()}
    </LocalizationProvider>
  )
}
