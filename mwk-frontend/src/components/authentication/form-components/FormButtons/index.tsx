import React from 'react'

import LoadingButton from '@mui/lab/LoadingButton'
import Button from '@mui/material/Button'

import { useLoad } from '../../../../hooks/useLoad'

type FormButtonsProps = {
  handleSubmit: any
  setShowErrors: (showErrors: boolean) => void
  loading?: boolean
  prevButton?: { prevStep: () => void }
  alterButton?: React.ReactNode
}

export const FormButtons: React.FC<FormButtonsProps> = ({
  handleSubmit,
  setShowErrors,
  loading,
  prevButton,
  alterButton,
}) => {
  const isLoad = useLoad(200)

  const generalButtonProps = {
    fullWidth: true,
    disabled: !isLoad,
    variant: 'contained',
  }

  const getSubmitButton = () => {
    if (loading) {
      return (
        <LoadingButton
          {...generalButtonProps}
          href="#"
          loading
          size="large"
          variant="contained"
          disabled={undefined}
          sx={{ mt: 3, mb: 2 }}
        >
          Loading...
        </LoadingButton>
      )
    }
    return (
      <Button
        {...generalButtonProps}
        size="large"
        type="submit"
        color="success"
        href="#"
        onClick={(e) => {
          handleSubmit(e)
          setShowErrors(true)
        }}
        sx={{ mt: 3, mb: 2 }}
        variant="contained"
      >
        Enter
      </Button>
    )
  }

  const getPrevButton = () => {
    if (!prevButton) {
      return null
    }

    return (
      <Button
        {...generalButtonProps}
        size="large"
        type="button"
        href="#"
        sx={{ mb: 2 }}
        variant="contained"
        onClick={prevButton.prevStep}
      >
        Back
      </Button>
    )
  }

  return (
    <React.Fragment>
      {getSubmitButton()}
      {getPrevButton()}
      {alterButton}
    </React.Fragment>
  )
}
