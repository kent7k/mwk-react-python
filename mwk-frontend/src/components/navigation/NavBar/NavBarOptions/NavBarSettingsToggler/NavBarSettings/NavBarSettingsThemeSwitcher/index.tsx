import React from 'react'
import { useDispatch } from 'react-redux'

import DarkModeOutlinedIcon from '@mui/icons-material/DarkModeOutlined'
import LightModeIcon from '@mui/icons-material/LightMode'
import ToggleButton from '@mui/material/ToggleButton'
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup'

import { useSelectedTheme } from '../../../../../../../hooks/useSelectedTheme'
import { setTheme } from '../../../../../../../store/slices/themeSlice'

export const NavBarSettingsThemeSwitcher = () => {
  const selectedTheme = useSelectedTheme()
  const dispatch: any = useDispatch()

  const iconsProps = {
    mr: 1,
  }

  const handleChange = (e, themeValue) => {
    dispatch(
      setTheme({
        theme: themeValue,
      })
    )
  }

  return (
    <ToggleButtonGroup
      onChange={handleChange}
      value={selectedTheme}
      fullWidth
      exclusive
      color="primary"
    >
      <ToggleButton fullWidth value="light">
        <LightModeIcon sx={iconsProps} />
        Light
      </ToggleButton>
      <ToggleButton fullWidth value="dark">
        <DarkModeOutlinedIcon sx={iconsProps} />
        Dark
      </ToggleButton>
    </ToggleButtonGroup>
  )
}
