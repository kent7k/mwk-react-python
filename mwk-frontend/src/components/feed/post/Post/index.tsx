import React, { useCallback, useEffect, useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { useNavigate, useParams } from 'react-router-dom'

import Grid from '@mui/material/Grid'

import { getTimeInfo } from '../../../../lib/feed'
import { getCommentsWrapper } from '../../../../store/actions/commentsActions/getCommentsWrapper'
import { getPost } from '../../../../store/actions/postsActions/getPost'
import { PostCard } from '../../card/PostCard'
import { FeedContainer } from '../../Feed/FeedContainer'
import { PostComments } from '../../post-comment/PostCommentsList/PostComments'
import { PostSkeleton } from '../PostSkeleton'

export const Post = () => {
  const { postId } = useParams()
  const { post, postNotFound } = useSelector((state: any) => state.posts)

  const [timeInfo, setTimeInfo] = useState([])

  const dispatch: any = useDispatch()
  const navigate = useNavigate()

  const fetchComments = useCallback(() => {
    dispatch(getCommentsWrapper(post.id))
  }, [dispatch, post])

  useEffect(() => {
    // FIXME
    dispatch(getPost(Number(postId)))
  }, [postId, dispatch])

  useEffect(() => {
    if (post) {
      setTimeInfo(getTimeInfo(post.created_at))
      fetchComments()
    }
  }, [post, dispatch, fetchComments])

  useEffect(() => {
    if (postNotFound) {
      navigate('/not-found/')
    }
  }, [postNotFound, navigate])

  return (
    <React.Fragment>
      <FeedContainer>
        {post && timeInfo.length ? (
          <Grid
            item
            sx={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              width: '100%',
            }}
          >
            <PostCard
              maxWidth={500}
              id={post.id}
              content={post.content}
              avatarAlt={post.author.first_name}
              avatarSrc={post.author.avatar}
              title={post.title}
              subheader={`${post.author.first_name} ${post.author.last_name}`}
              timesince={timeInfo[0]}
              time={timeInfo[1]}
              viewsCount={post.viewers_count}
              likesCount={post.liked_count}
              commentsCount={post.comments_count}
              isLiked={post.is_user_liked_post}
              images={post.images}
            />
          </Grid>
        ) : (
          <PostSkeleton />
        )}
      </FeedContainer>
      <PostComments title="Comment" />
    </React.Fragment>
  )
}
