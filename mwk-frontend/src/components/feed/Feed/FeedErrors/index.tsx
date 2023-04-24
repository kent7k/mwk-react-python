import React from 'react'
import { useDispatch, useSelector } from 'react-redux'

import Alert from '@mui/material/Alert'
import Grid from '@mui/material/Grid'

import { showComponent } from '../../../../lib'
import { shiftAPIErrors } from '../../../../store/slices/APIErrorsSlice'

export function FeedErrors() {
  const APIErrors = useSelector((state: any) => state.APIErrors.APIErrors)
  const dispatch: any = useDispatch()

  const handleClose = () => {
    dispatch(shiftAPIErrors())
  }

  return showComponent(
    <Grid
      item
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
      }}
    >
      <Alert
        sx={{
          maxWidth: 400,
        }}
        onClose={handleClose}
        severity="error"
      >
        {APIErrors[0]}
      </Alert>
    </Grid>,
    APIErrors.length
  )
}
