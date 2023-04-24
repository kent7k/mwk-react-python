import React from 'react'

import Autocomplete from '@mui/material/Autocomplete'
import Box from '@mui/material/Box'
import CircularProgress from '@mui/material/CircularProgress'
import TextField from '@mui/material/TextField'

interface Props {
  compareFunc?: (option: any, value: any) => boolean
  getOptionLabel?: (option: any) => string
  render?: (renderProps: any, option: any) => React.ReactNode
  label?: string
  textFieldProps?: any
  loading: boolean
  filterOptions?: any
  disabled?: boolean
  options: object[]
  handleChange: any
  valueProps: any
}

export const FormSelect: React.FC<Props> = ({
  compareFunc,
  getOptionLabel,
  // render,
  label,
  textFieldProps,
  loading,
  filterOptions,
  disabled,
  options,
  handleChange,
  valueProps,
}) => {
  const compare = (option, value) => {
    if (compareFunc) {
      return compareFunc(option, value)
    }
    return option === value
  }

  const getLabel = (option) => {
    if (getOptionLabel) {
      return getOptionLabel(option)
    }
    return option
  }

  const render = (renderProps, option) => {
    if (typeof renderProps.render === 'function') {
      return renderProps.render(renderProps, option)
    }
    return (
      <Box component="li" sx={{ '& > img': { mr: 2, flexShrink: 0 } }}>
        {option}
      </Box>
    )
  }

  const renderInput = (params) => {
    const getEndAdornment = () => {
      if (loading) {
        return <CircularProgress color="inherit" size={20} />
      }
      return null
    }

    return (
      <TextField
        {...params}
        label={label || ''}
        InputProps={{
          ...params.InputProps,
          endAdornment: (
            <React.Fragment>
              {getEndAdornment()}
              {params.InputendAdornment}
            </React.Fragment>
          ),
        }}
        {...textFieldProps}
      />
    )
  }

  return (
    <Autocomplete
      loading={loading}
      disablePortal
      filterOptions={filterOptions}
      disabled={disabled}
      isOptionEqualToValue={compare}
      options={!options.length ? [] : options}
      fullWidth
      getOptionLabel={getLabel}
      onChange={handleChange}
      value={valueProps || null}
      renderOption={render}
      renderInput={renderInput}
    />
  )
}
