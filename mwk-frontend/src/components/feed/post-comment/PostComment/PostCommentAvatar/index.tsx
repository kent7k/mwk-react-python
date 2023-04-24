import React from 'react'

import Avatar from '@mui/material/Avatar'
import ListItemAvatar from '@mui/material/ListItemAvatar'

export const PostCommentAvatar = ({
  alt = 'Avatar',
  src = '/static/images/avatar/1.jpg',
}) => (
  <ListItemAvatar>
    <Avatar alt={alt} src={src} />
  </ListItemAvatar>
)
