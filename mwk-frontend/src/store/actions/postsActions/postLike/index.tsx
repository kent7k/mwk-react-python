import { createAsyncThunk } from '@reduxjs/toolkit'

import FeedAPI from '../../../../api/feed'
import { parseAPIAxiosErrors } from '../../../../lib'
import { setAPIErrors } from '../../../slices/APIErrorsSlice'

export const postLike = createAsyncThunk(
  'posts/likePost',
  async (postId: number, { rejectWithValue, dispatch, getState }) => {
    try {
      const { user } = getState() as any

      const config = {
        headers: {
          Authorization: `Token ${user.token}`,
        },
      }

      const response = await FeedAPI.postLike({ post: postId }, config)
      const { action } = response.data

      return {
        postId,
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
        postId,
      })
    }
  }
)
