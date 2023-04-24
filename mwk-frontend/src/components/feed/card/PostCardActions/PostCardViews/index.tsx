import React from 'react'

import VisibilityIcon from '@mui/icons-material/Visibility'
import IconButton from '@mui/material/IconButton'
import Typography from '@mui/material/Typography'

type Props = {
  viewsCount: number
}

export const PostCardViews: React.FC<Props> = ({ viewsCount }) => (
  <div className="flexAlignBox">
    <Typography
      sx={{
        lineHeight: 'normal',
      }}
      variant="body2"
    >
      {viewsCount}
    </Typography>
    <IconButton>
      <VisibilityIcon fontSize="small" />
    </IconButton>
  </div>
)
