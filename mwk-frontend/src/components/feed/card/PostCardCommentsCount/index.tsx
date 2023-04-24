import React from 'react'

import CommentIcon from '@mui/icons-material/Comment'
import IconButton from '@mui/material/IconButton'
import Typography from '@mui/material/Typography'

type Props = {
  href: string
  commentsCount: number
}

export const PostCardCommentsCount: React.FC<Props> = ({
  href,
  commentsCount,
}) => (
  <div className="flexAlignBox">
    <IconButton sx={{ ml: 1 }} href={href} aria-label="comments count">
      <CommentIcon />
    </IconButton>
    <Typography
      sx={{
        lineHeight: 'normal',
      }}
      variant="body2"
    >
      {commentsCount}
    </Typography>
  </div>
)
