import React from 'react'
import { useDispatch, useSelector } from 'react-redux'

import Card from '@mui/material/Card'

import { postLike } from '../../../../store/actions/postsActions/postLike/index'
import { PostCardActions as CardActions } from '../PostCardActions'
import { PostCardContent as CardContent } from '../PostCardContent'
import { PostCardHeader as CardHeader } from '../PostCardHeader'
import { PostCardMedia as CardMedia } from '../PostCardMedia'
import { PostCardSkeleton } from '../PostCardSkeleton'

type Props = {
  maxWidth?: number
  loading?: boolean
  avatarAlt: string
  avatarSrc: string
  title: string
  subheader: string
  images: string[]
  content: string
  timesince: string
  time: string
  likesCount: number
  commentsCount: number
  isLiked: boolean
  viewsCount: number
  id: string
}

export const PostCard: React.FC<Props> = ({
  maxWidth,
  loading,
  avatarAlt,
  avatarSrc,
  title,
  subheader,
  images,
  content,
  timesince,
  time,
  likesCount,
  commentsCount,
  isLiked,
  viewsCount,
  id,
}) => {
  const dispatch: any = useDispatch()
  // TODO: type RouteState
  const { likePendingPosts } = useSelector((state: any) => state.posts)

  const handleLikeClick = () => {
    // FIXME
    dispatch(postLike(Number(id)))
  }

  const postUrl = `/feed/${id}`

  return (
    <Card sx={{ maxWidth: maxWidth || 345, width: '100%' }}>
      {loading ? (
        <PostCardSkeleton />
      ) : (
        <React.Fragment>
          <CardHeader
            avatarAlt={avatarAlt}
            avatarSrc={avatarSrc}
            title={title}
            href={postUrl}
            subheader={subheader}
          />
          <CardMedia images={images} />
          <CardContent content={content} />
          <CardActions
            handleLikeClick={handleLikeClick}
            timesince={timesince}
            time={time}
            likeDisabled={id in likePendingPosts}
            likesCount={likesCount}
            commentsCount={commentsCount}
            commentsHref={postUrl}
            isLiked={isLiked}
            viewsCount={viewsCount}
          />
        </React.Fragment>
      )}
    </Card>
  )
}
