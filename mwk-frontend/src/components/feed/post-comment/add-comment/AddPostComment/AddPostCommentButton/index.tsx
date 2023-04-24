import React from 'react'
import { useSelector } from 'react-redux'

import SendIcon from '@mui/icons-material/Send'
import Box from '@mui/material/Box'
import CircularProgress from '@mui/material/CircularProgress'
import IconButton from '@mui/material/IconButton'

export const AddPostCommentButton = () => {
  const { addCommentLoading: loading } = useSelector(
    (state: any) => state.comments
  )

  return (
    <Box sx={{ ml: 1.5 }}>
      {loading ? (
        <CircularProgress sx={{ mt: 0.5 }} size="1.3rem" />
      ) : (
        <IconButton type="submit" edge="end">
          <SendIcon />
        </IconButton>
      )}
    </Box>
  )
}
