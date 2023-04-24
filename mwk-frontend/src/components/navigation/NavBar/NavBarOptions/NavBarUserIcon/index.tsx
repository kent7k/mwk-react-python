import React from 'react'

import Avatar from '@mui/material/Avatar'
import Box from '@mui/material/Box'
import Skeleton from '@mui/material/Skeleton'

type Props = {
  loading: boolean
  alt: string
  src: string
}

export const NavBarUserIcon: React.FC<Props> = ({ loading, alt, src }) => (
  <Box sx={{ flexGrow: 0 }}>
    {loading ? (
      <Skeleton animation="wave" variant="circular" width={40} height={40} />
    ) : (
      <Avatar alt={alt} src={src} />
    )}
  </Box>
)
