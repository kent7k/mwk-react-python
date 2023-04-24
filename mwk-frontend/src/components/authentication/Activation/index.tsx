import React, { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { NavLink, useParams } from 'react-router-dom'

import CheckCircleIcon from '@mui/icons-material/CheckCircle'
import DownloadingIcon from '@mui/icons-material/Downloading'
import ErrorIcon from '@mui/icons-material/Error'
import Container from '@mui/material/Container'
import Grid from '@mui/material/Grid'
import Typography from '@mui/material/Typography'

import { userActivate } from '../../../store/actions'

import './activation.css'

export const Activation = () => {
  const { uid, token } = useParams()
  const dispatch: any = useDispatch()
  const { success, rejected, errors } = useSelector((state: any) => state.user)

  useEffect(() => {
    // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
    dispatch(userActivate({ uid: uid!, token: token! }))
  }, [dispatch, token, uid])

  const getIcon = () => {
    if (success) {
      return <CheckCircleIcon fontSize="large" color="success" />
    }
    if (rejected) {
      return <ErrorIcon fontSize="large" color="error" />
    }

    return <DownloadingIcon fontSize="large" color="primary" />
  }

  const getText = () => {
    const successText = (
      <NavLink to="/login/">
        You have successfully activated your account! Now you can log in.
      </NavLink>
    )
    const loadingText = 'Activation in progress...'

    if (success) {
      return successText
    }
    if (rejected) {
      return errors[0]
    }

    return loadingText
  }

  return (
    <Container
      sx={{
        height: '100vh',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
      }}
      maxWidth="lg"
    >
      <Grid
        justifyContent="center"
        alignItems="center"
        container
        spacing={0}
        direction="column"
      >
        <Grid item xs={6}>
          {getIcon()}
        </Grid>
        <Grid item xs={6}>
          <Typography variant="h6">{getText()}</Typography>
        </Grid>
      </Grid>
    </Container>
  )
}
