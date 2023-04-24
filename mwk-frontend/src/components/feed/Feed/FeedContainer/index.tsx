import React from 'react'

import Container from '@mui/material/Container'
import Grid from '@mui/material/Grid'

import { NavBar } from '../../../navigation/NavBar'

export const FeedContainer = ({ children }) => (
  <React.Fragment>
    <NavBar />
    <Container
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
      }}
      component="main"
      maxWidth="xl"
    >
      <Grid
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          width: '100%',
          pt: 12,
          mb: 3,
        }}
        direction="column"
        container
        spacing={2}
      >
        {children}
      </Grid>
    </Container>
  </React.Fragment>
)
