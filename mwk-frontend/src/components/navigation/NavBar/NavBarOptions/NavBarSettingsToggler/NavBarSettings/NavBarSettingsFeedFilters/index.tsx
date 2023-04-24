import React, { useState } from 'react'

import Button from '@mui/material/Button'

import { NavBarSettingsFeedFiltersDialog } from './NavBarSettingsFeedFiltersDialog'

export const NavBarSettingsFeedFilters = () => {
  const [open, setOpen] = useState(false)

  const handleClose = () => {
    setOpen(false)
  }

  const handleOpen = () => {
    setOpen(true)
  }

  return (
    <React.Fragment>
      <NavBarSettingsFeedFiltersDialog open={open} handleClose={handleClose} />
      <Button onClick={handleOpen} fullWidth variant="contained">
        Open post filters
      </Button>
    </React.Fragment>
  )
}
