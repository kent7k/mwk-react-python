import { createAsyncThunk } from '@reduxjs/toolkit'

import FeedAPI from '../../../../api/feed'
import { parseAPIAxiosErrors } from '../../../../lib'
import { setAPIErrors } from '../../../slices/APIErrorsSlice'

interface AddCommentResponse {
  comment: any
  parent: any
}

export const addComment = createAsyncThunk<
  AddCommentResponse, // 戻り値の型
  any,
  {
    rejectValue: {
      APIErrors: any
    }
  }
>(
  'comments/addComment',
  async (data, { rejectWithValue, dispatch, getState }) => {
    try {
      const { user } = getState() as any

      const config = {
        headers: {
          Authorization: `Token ${user.token}`,
        },
      }

      const response = await FeedAPI.addComment(data, config)

      const comment = response.data

      return {
        comment,
        parent: data.parent,
      }
    } catch (err) {
      const APIErrors = parseAPIAxiosErrors(err)

      dispatch(
        setAPIErrors({
          APIErrors,
        })
      )

      return rejectWithValue({
        APIErrors,
      })
    }
  }
)
