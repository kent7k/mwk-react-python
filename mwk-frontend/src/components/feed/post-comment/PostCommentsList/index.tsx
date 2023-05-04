import React from 'react'
import { useSelector } from 'react-redux'

import List from '@mui/material/List'

import { getTimeInfo } from '../../../../lib/feed'
import { PostComment } from '../PostComment'

import { PostCommentsSkeleton } from './PostCommentsSkeleton'

export const PostCommentsList = () => {
  const { postComments, commentsLoading } = useSelector(
    (state: any) => state.comments
  )

  return (
    <List
      sx={{
        width: '100%',
        pb: 0,
        mb: 0.5,
      }}
      className="comments"
    >
      {postComments
        ? postComments.map((el) => {
            const getCommentProps = (comment) => ({
              id: comment.id,
              username: `${comment.author.first_name} ${comment.author.last_name}`,
              text: comment.body,
              timesince: getTimeInfo(comment.created_at).join(' at '),
              likesCount: comment.liked_count,
              avatarAlt: comment.author.first_name,
              avatarSrc: comment.author.avatar,
              isLiked: comment.is_user_liked_comment,
              replies: comment.replies,
              repliesCnt: comment.replies_count - comment.replies.length,
            })

            return (
              <li key={el.id} className="comment">
                <PostComment {...getCommentProps(el)} />
              </li>
            )
          })
        : null}
      {commentsLoading && <PostCommentsSkeleton />}
    </List>
  )
}
