import React from 'react'

import FavoriteIcon from '@mui/icons-material/Favorite'
import IconButton from '@mui/material/IconButton'
import Typography from '@mui/material/Typography'

export const PostCommentLike = ({
  likesCount,
  isLiked,
  disabled,
  handleLikeClick,
}) => (
  <div className="flexAlignBox" style={{ paddingTop: 'inherit' }}>
    <IconButton
      disabled={disabled}
      onClick={handleLikeClick}
      aria-label="like comment"
    >
      <FavoriteIcon fontSize="small" color={isLiked ? 'error' : undefined} />
    </IconButton>
    <Typography
      sx={{
        lineHeight: 'normal',
      }}
      variant="body2"
    >
      {likesCount}
    </Typography>
  </div>
)
