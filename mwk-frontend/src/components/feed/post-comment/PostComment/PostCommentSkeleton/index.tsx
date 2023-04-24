import React from 'react'

import ListItem from '@mui/material/ListItem'
import ListItemAvatar from '@mui/material/ListItemAvatar'
import ListItemText from '@mui/material/ListItemText'
import Skeleton from '@mui/material/Skeleton'

export const PostCommentSkeleton = () => (
  <ListItem component="div" alignItems="flex-start" sx={{ pb: 0 }}>
    <ListItemAvatar>
      <Skeleton animation="wave" variant="circular" width={40} height={40} />
    </ListItemAvatar>
    <ListItemText
      primary={<Skeleton animation="wave" width="40%" />}
      secondary={
        <Skeleton
          animation="wave"
          variant="rectangular"
          width="100%"
          height={60}
        />
      }
      sx={{ mb: 0 }}
      disableTypography
    />
  </ListItem>
)
