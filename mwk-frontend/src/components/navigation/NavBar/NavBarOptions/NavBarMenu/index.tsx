import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'

import MenuIcon from '@mui/icons-material/Menu'
import Box from '@mui/material/Box'
import Button from '@mui/material/Button'
import IconButton from '@mui/material/IconButton'
import Menu from '@mui/material/Menu'
import MenuItem from '@mui/material/MenuItem'
import Typography from '@mui/material/Typography'

export function NavBarMenu(props) {
  const [anchorElNav, setAnchorElNav] = useState(null)
  const navigate = useNavigate()

  const handleOpenNavMenu = (event) => {
    setAnchorElNav(event.currentTarget)
  }

  const handleCloseNavMenu = () => {
    setAnchorElNav(null)
  }

  const getPages = () =>
    props.pages.map((page) => {
      if (props.isMobile) {
        return (
          <MenuItem
            key={page.title}
            onClick={() => {
              handleCloseNavMenu()
              navigate(page.href)
            }}
          >
            <Typography textAlign="center">{page.title}</Typography>
          </MenuItem>
        )
      }

      return (
        <Button
          key={page.title}
          onClick={() => {
            navigate(page.href)
          }}
          sx={{
            my: 2,
            color: 'white',
            display: 'block',
          }}
        >
          {page.title}
        </Button>
      )
    })

  const getMenu = () => {
    if (props.isMobile) {
      return (
        <Box sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } }}>
          <IconButton
            onClick={handleOpenNavMenu}
            size="large"
            aria-haspopup="true"
            color="inherit"
          >
            <MenuIcon />
          </IconButton>
          <Menu
            anchorOrigin={{
              vertical: 'bottom',
              horizontal: 'left',
            }}
            keepMounted
            transformOrigin={{
              vertical: 'top',
              horizontal: 'left',
            }}
            anchorEl={anchorElNav}
            open={!!anchorElNav}
            onClose={handleCloseNavMenu}
            sx={{
              display: { xs: 'block', md: 'none' },
            }}
          >
            {getPages()}
          </Menu>
        </Box>
      )
    }

    return (
      <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' } }}>
        {getPages()}
      </Box>
    )
  }

  return getMenu()
}
