import React from 'react'

import FavoriteIcon from '@mui/icons-material/Favorite'
import IconButton from '@mui/material/IconButton'
import Typography from '@mui/material/Typography'

type Props = {
  disabled: boolean
  handleLikeClick: () => void
  isLiked: boolean
  likesCount: number
}

export const PostCardLike: React.FC<Props> = ({
  disabled,
  handleLikeClick,
  isLiked,
  likesCount,
}) => (
  <div className="flexAlignBox">
    <IconButton disabled={disabled} onClick={handleLikeClick} aria-label="like">
      <FavoriteIcon color={isLiked ? 'error' : undefined} />
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
