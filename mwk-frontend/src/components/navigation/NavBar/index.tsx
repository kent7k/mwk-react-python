import React from 'react'

import AppBar from '@mui/material/AppBar'
import Box from '@mui/material/Box'
import Container from '@mui/material/Container'

import { NavBarOptions } from './NavBarOptions'

export const NavBar = () => {
  const pages = [
    {
      title: 'Feed',
      href: '/feed/',
    },
  ]

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="fixed">
        <Container maxWidth="xl">
          <NavBarOptions pages={pages} />
        </Container>
      </AppBar>
    </Box>
  )
}
