import { createAsyncThunk } from '@reduxjs/toolkit'

import { getCommentDescendants } from '../getCommentDescendants'

export const getCommentDescendantsWrapper = createAsyncThunk(
  'comments/getCommentDescendantsWrapper',
  async (commentId: number, { dispatch, getState }) => {
    const { descendantsLoading } = (getState() as any).comments

    if (!Object.prototype.hasOwnProperty.call(descendantsLoading, commentId)) {
      dispatch(getCommentDescendants(commentId))
    }
  }
)
