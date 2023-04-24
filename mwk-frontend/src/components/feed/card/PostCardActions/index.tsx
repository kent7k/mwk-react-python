import React from 'react'

import CardActions from '@mui/material/CardActions'
import Divider from '@mui/material/Divider'
import Typography from '@mui/material/Typography'

import { PostCardCommentsCount as Comments } from '../PostCardCommentsCount'
import { PostCardLike as Likes } from '../PostCardLike'

import { PostCardViews as Views } from './PostCardViews'

type PostCardActionsProps = {
  time: string
  likeDisabled: boolean
  handleLikeClick: () => void
  isLiked: boolean
  likesCount: number
  commentsHref: string
  commentsCount: number
  timesince: string
  viewsCount: number
}

export const PostCardActions: React.FC<PostCardActionsProps> = ({
  time,
  likeDisabled,
  handleLikeClick,
  isLiked,
  likesCount,
  commentsHref,
  commentsCount,
  timesince,
  viewsCount,
}) => {
  const timeParts = time.split(':')
  const zeroFilledMinutes = timeParts[1].padStart(2, '0')
  const time2 = `${timeParts[0]}:${zeroFilledMinutes}`

  return (
    <React.Fragment>
      <Divider variant="middle" />
      <CardActions
        sx={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}
      >
        <div className="flexAlignBox">
          <Likes
            disabled={likeDisabled}
            handleLikeClick={handleLikeClick}
            isLiked={isLiked}
            likesCount={likesCount}
          />
          <Comments href={commentsHref} commentsCount={commentsCount} />
        </div>
        <div className="flexAlignBox">
          <Typography color="rgba(255, 255, 255, 0.7)" variant="body2">
            {timesince} at {time2}
          </Typography>
        </div>
        <Views viewsCount={viewsCount} />
      </CardActions>
    </React.Fragment>
  )
}
