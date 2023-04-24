import React from 'react'
import { useSelector } from 'react-redux'

import Box from '@mui/material/Box'
import Button from '@mui/material/Button'

export const PostCommentShowMoreReplies = ({
  repliesCnt,
  getDescendants,
  commentId,
}) => {
  const { descendantsPage } = useSelector((state: any) => state.comments)

  return repliesCnt && repliesCnt > 0 && !(commentId in descendantsPage) ? (
    <Box display="flex" justifyContent="center">
      <Button onClick={getDescendants} sx={{ mt: 2 }} size="small">
        Show {repliesCnt} more replies
      </Button>
    </Box>
  ) : null
}
