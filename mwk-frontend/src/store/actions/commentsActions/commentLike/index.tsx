import { createAsyncThunk } from '@reduxjs/toolkit'

import FeedAPI from '../../../../api/feed'
import { parseAPIAxiosErrors } from '../../../../lib'
import { setAPIErrors } from '../../../slices/APIErrorsSlice'

export const commentLike = createAsyncThunk(
  'comments/likeComment',
  async (commentId: number, { rejectWithValue, dispatch, getState }) => {
    try {
      const { user } = getState() as any

      const config = {
        headers: {
          Authorization: `Token ${user.token}`,
        },
      }

      const response = await FeedAPI.commentLike({ comment: commentId }, config)
      const { action } = response.data

      return {
        commentId,
        action,
      }
    } catch (err) {
      const APIErrors = parseAPIAxiosErrors(err)

      dispatch(
        setAPIErrors({
          APIErrors,
        })
      )

      return rejectWithValue({
        commentId,
      })
    }
  }
)
