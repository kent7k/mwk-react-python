import React from 'react'

import ListItemText from '@mui/material/ListItemText'
import Typography from '@mui/material/Typography'

export const PostCommentText = ({ username, text, actions }) => (
  <ListItemText
    primary={username}
    sx={{ mb: 0 }}
    disableTypography
    secondary={
      <React.Fragment>
        <Typography variant="body2">{text}</Typography>
        {actions}
      </React.Fragment>
    }
  />
)
