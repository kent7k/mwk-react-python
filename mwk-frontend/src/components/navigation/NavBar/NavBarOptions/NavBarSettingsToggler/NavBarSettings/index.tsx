import React from 'react'

import CloseIcon from '@mui/icons-material/Close'
import Box from '@mui/material/Box'
import Divider from '@mui/material/Divider'
import Drawer from '@mui/material/Drawer'
import IconButton from '@mui/material/IconButton'
import Typography from '@mui/material/Typography'

import { NavBarSettingsFeedFilters } from './NavBarSettingsFeedFilters'
import { NavBarSettingsSection } from './NavBarSettingsSection'
import { NavBarSettingsThemeSwitcher } from './NavBarSettingsThemeSwitcher'

type Props = {
  open: boolean
  handleClose: () => void
}

export const NavBarSettings: React.FC<Props> = ({ open, handleClose }) => (
  <Drawer variant="temporary" anchor="right" open={open} onClose={handleClose}>
    <Box
      display="flex"
      alignItems="center"
      padding={2}
      justifyContent="space-between"
    >
      <Typography variant="body1">Setting</Typography>
      <IconButton onClick={handleClose}>
        <CloseIcon />
      </IconButton>
    </Box>
    <Divider />
    <Box px={2}>
      <NavBarSettingsSection title="Тема">
        <NavBarSettingsThemeSwitcher />
      </NavBarSettingsSection>
      <NavBarSettingsSection title="Feed">
        <NavBarSettingsFeedFilters />
      </NavBarSettingsSection>
    </Box>
  </Drawer>
)
