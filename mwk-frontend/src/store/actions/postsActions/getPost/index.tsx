import { createAsyncThunk } from '@reduxjs/toolkit'

import FeedAPI from '../../../../api/feed'
import { parseAPIAxiosErrors } from '../../../../lib'
import { setAPIErrors } from '../../../slices/APIErrorsSlice'

export const getPost = createAsyncThunk(
  'posts/getPost',
  async (postId: number, { rejectWithValue, dispatch, getState }) => {
    try {
      const { user } = getState() as any

      const config = {
        headers: {
          Authorization: `Token ${user.token}`,
        },
      }

      const response = await FeedAPI.getPost(postId, config)
      const post = response.data

      return {
        post,
      }
    } catch (err: any) {
      const APIErrors = parseAPIAxiosErrors(err)

      dispatch(
        setAPIErrors({
          APIErrors,
        })
      )

      return rejectWithValue({
        status: err.response.status,
      })
    }
  }
)
