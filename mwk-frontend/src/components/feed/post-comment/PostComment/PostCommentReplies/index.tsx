import React from 'react'
import { useDispatch, useSelector } from 'react-redux'

import Box from '@mui/material/Box'

import { getCommentDescendantsWrapper } from '../../../../../store/actions/commentsActions/getCommentDescendantsWrapper'
import { FeedInfiniteScroll } from '../../../FeedInfiniteScroll'
import { PostCommentRepliesList } from '../PostCommentRepliesList'

import { PostCommentRepliesSkeleton } from './PostCommentRepliesSkeleton'
import { PostCommentShowMoreReplies } from './PostCommentShowMoreReplies'

export const PostCommentReplies = ({ replies, repliesCnt, commentId }) => {
  const dispatch: any = useDispatch()
  const { descendantsPage, descendantsLoading } = useSelector(
    (state: any) => state.comments
  )

  const getDescendants = () => {
    dispatch(getCommentDescendantsWrapper(commentId))
  }

  return replies.length ? (
    <Box sx={{ pl: 7 }} className="comment__replies">
      <PostCommentRepliesList replies={replies} />
      {descendantsLoading[commentId] ? <PostCommentRepliesSkeleton /> : null}
      <PostCommentShowMoreReplies
        repliesCnt={repliesCnt}
        commentId={commentId}
        getDescendants={getDescendants}
      />
      {descendantsPage[commentId] ? (
        <FeedInfiniteScroll onIntersecting={getDescendants} />
      ) : null}
    </Box>
  ) : null
}
