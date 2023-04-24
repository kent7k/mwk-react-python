import React from 'react'
import { useDispatch, useSelector } from 'react-redux'

import Alert from '@mui/material/Alert'
import Box from '@mui/material/Box'
import Container from '@mui/material/Container'
import Grid from '@mui/material/Grid'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'

import { showComponent } from '../../../lib'
import { shiftAPIErrors } from '../../../store/slices/APIErrorsSlice'
import { FormButtons as Buttons } from '../form-components/FormButtons'

import './authentication.css'

interface FormProps {
  title: string
  fields: React.ReactNode
  buttons: Record<string, unknown>
  handleSubmit: () => void
  setShowErrors: (showErrors: boolean) => void
  message?: string
  setMessage?: (message: string) => void
}

export const Form: React.FC<FormProps> = ({
  title,
  message,
  fields,
  buttons,
  handleSubmit,
  setShowErrors,
  setMessage,
}: FormProps) => {
  const APIErrors = useSelector((state: any) => state.APIErrors.APIErrors)
  const dispatch: any = useDispatch()

  const handleClose = () => {
    dispatch(shiftAPIErrors())
  }

  const handleCloseMessage = () => {
    if (setMessage) {
      setMessage('')
    }
  }

  return (
    <Container
      sx={{
        height: '100vh',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
      }}
      component="main"
      maxWidth="xs"
    >
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          width: '100%',
        }}
      >
        {showComponent(
          <Typography variant="h5">{title}</Typography>,
          !APIErrors.length && !message
        )}

        {showComponent(
          <Grid item xs={12}>
            <Alert onClose={handleClose} severity="error">
              {APIErrors[0]}
            </Alert>
          </Grid>,
          APIErrors.length && !message
        )}

        {showComponent(
          <Grid item xs={12}>
            <Alert onClose={handleCloseMessage} severity="info">
              {message}
            </Alert>
          </Grid>,
          message
        )}

        <Box
          component="form"
          noValidate
          onSubmit={handleSubmit}
          sx={{ mt: 3, width: '100%' }}
        >
          <Stack spacing={2}>{fields}</Stack>
          <Buttons
            handleSubmit={handleSubmit}
            setShowErrors={setShowErrors}
            {...buttons}
          />
        </Box>
      </Box>
    </Container>
  )
}
