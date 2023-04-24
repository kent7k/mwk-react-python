import React from 'react'
import { useDispatch } from 'react-redux'

import Box from '@mui/material/Box'
import Button from '@mui/material/Button'
import Typography from '@mui/material/Typography'

import { userLogout } from '../../../store/actions'

export const Logout = () => {
  const dispatch: any = useDispatch()
  const handleClick = () => {
    dispatch(userLogout())
  }

  return (
    <Box
      sx={{
        width: '100%',
        height: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        flexDirection: 'column',
      }}
    >
      <Typography variant="h4" gutterBottom>
        Logout?
      </Typography>
      <Button variant="contained" onClick={handleClick}>
        Logout
      </Button>
    </Box>
  )
}
