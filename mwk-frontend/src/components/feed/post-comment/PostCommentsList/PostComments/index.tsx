import React, { useCallback } from 'react'
import { useDispatch, useSelector } from 'react-redux'

import Container from '@mui/material/Container'
import Divider from '@mui/material/Divider'
import Paper from '@mui/material/Paper'

import { PostCommentsList } from '..'
import { getCommentsWrapper } from '../../../../../store/actions/commentsActions/getCommentsWrapper'
import { FeedInfiniteScroll } from '../../../FeedInfiniteScroll'
import { AddPostComment } from '../../add-comment/AddPostComment'

import './comments.css'

type Props = {
  title: React.ReactNode
}

export const PostComments: React.FC<Props> = ({ title }) => {
  const { postComments, commentsLoading } = useSelector(
    (state: any) => state.comments
  )
  const { post } = useSelector((state: any) => state.posts)

  const dispatch: any = useDispatch()

  const fetchComments = useCallback(() => {
    dispatch(getCommentsWrapper(post.id))
  }, [dispatch, post])

  return (
    <Container
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        mb: 3,
      }}
      maxWidth="xl"
    >
      {title}
      <Paper
        sx={{
          width: '100%',
          maxWidth: 500,
          p: 1,
        }}
      >
        <AddPostComment id="add-comment" />
        {!postComments.length && !commentsLoading ? null : (
          <React.Fragment>
            <Divider variant="fullWidth" sx={{ mx: -1, mt: 1 }} />
            <PostCommentsList />
          </React.Fragment>
        )}
      </Paper>
      {!postComments.length ? null : (
        <FeedInfiniteScroll onIntersecting={fetchComments} />
      )}
    </Container>
  )
}
