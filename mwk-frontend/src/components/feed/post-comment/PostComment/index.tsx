import React, { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'

import Box from '@mui/material/Box'
import Collapse from '@mui/material/Collapse'
import Divider from '@mui/material/Divider'
import ListItem from '@mui/material/ListItem'

import { commentLike } from '../../../../store/actions/commentsActions/commentLike'
import { AddPostComment } from '../add-comment/AddPostComment'

import { PostCommentActions } from './PostCommentActions'
import { PostCommentAvatar } from './PostCommentAvatar'
import { PostCommentReplies } from './PostCommentReplies'
import { PostCommentText } from './PostCommentText'

export const PostComment = ({
  id,
  username,
  text,
  timesince,
  likesCount,
  avatarAlt,
  avatarSrc,
  isLiked,
  replies,
  repliesCnt,
}) => {
  const dispatch: any = useDispatch()
  const { likePendingComments } = useSelector((state: any) => state.comments)

  const [showAddCommentForm, setShowAddCommentForm] = useState(false)

  const handleLikeClick = () => {
    dispatch(commentLike(id))
  }

  const handleReplyClick = () => {
    setShowAddCommentForm(!showAddCommentForm)
  }

  return (
    <React.Fragment>
      <ListItem component="div" alignItems="flex-start" sx={{ pb: 0 }}>
        <PostCommentAvatar alt={avatarAlt} src={avatarSrc} />
        <PostCommentText
          username={username}
          text={text}
          actions={
            <PostCommentActions
              timesince={timesince}
              likesCount={likesCount}
              handleLikeClick={handleLikeClick}
              handleReplyClick={handleReplyClick}
              isLikeDisabled={id in likePendingComments}
              isLiked={isLiked}
            />
          }
        />
      </ListItem>
      <Divider sx={{ mr: 2 }} variant="inset" className="comment__divider" />
      <Collapse in={showAddCommentForm}>
        <Box sx={{ pl: 7, mt: 1 }}>
          <AddPostComment parent={id} id={`reply-${id}`} />
        </Box>
      </Collapse>
      <PostCommentReplies
        replies={replies}
        repliesCnt={repliesCnt}
        commentId={id}
      />
    </React.Fragment>
  )
}
