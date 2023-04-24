import React from 'react'
import { useSelector } from 'react-redux'

import Toolbar from '@mui/material/Toolbar'

import { NavBarMenu } from './NavBarMenu'
import { NavBarSettingsToggler } from './NavBarSettingsToggler'
import { NavBarUserIcon } from './NavBarUserIcon'

export const NavBarOptions = (props) => {
  const { pages } = props

  const { first_name, avatar } = useSelector(
    (state: any) => state.user.userInfo
  )
  const { loading } = useSelector((state: any) => state.user)

  const navBarMenuProps = {
    pages,
  }

  return (
    <Toolbar disableGutters>
      <NavBarMenu {...navBarMenuProps} isMobile />
      <NavBarMenu {...navBarMenuProps} isMobile={false} />
      <NavBarSettingsToggler />
      <NavBarUserIcon loading={loading} src={avatar} alt={first_name} />
    </Toolbar>
  )
}
