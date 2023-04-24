import { createAsyncThunk } from '@reduxjs/toolkit'

import { getComments } from '../getComments'

export const getCommentsWrapper = createAsyncThunk(
  'comments/getCommentsWrapper',
  async (postId: number, { dispatch, getState }) => {
    const { commentsLoading } = (getState() as any).comments

    if (!commentsLoading) {
      dispatch(getComments(postId))
    }
  }
)
