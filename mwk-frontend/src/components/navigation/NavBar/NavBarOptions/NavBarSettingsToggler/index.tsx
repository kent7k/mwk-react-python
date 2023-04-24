import React, { useState } from 'react'

import SettingsOutlinedIcon from '@mui/icons-material/SettingsOutlined'
import IconButton from '@mui/material/IconButton'

import { NavBarSettings } from './NavBarSettings'

export const NavBarSettingsToggler = () => {
  const [open, setOpen] = useState(false)

  const handleOpen = () => {
    setOpen(true)
  }

  const handleClose = () => {
    setOpen(false)
  }

  return (
    <React.Fragment>
      <IconButton onClick={handleOpen} sx={{ mr: 1 }} color="inherit">
        <SettingsOutlinedIcon />
      </IconButton>
      <NavBarSettings open={open} handleClose={handleClose} />
    </React.Fragment>
  )
}
