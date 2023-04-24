import { createAsyncThunk } from '@reduxjs/toolkit'

import FeedAPI from '../../../../api/feed'
import { parseAPIAxiosErrors } from '../../../../lib'
import { setAPIErrors } from '../../../slices/APIErrorsSlice'

export const getComments = createAsyncThunk(
  'comments/getComments',
  async (postId: number, { rejectWithValue, dispatch, getState }) => {
    try {
      const { user, comments: commentsState } = getState() as any

      const config = {
        headers: {
          Authorization: `Token ${user.token}`,
        },
      }

      const { nextPage: page } = commentsState

      if (!page) {
        return {
          comments: [],
          nextPage: null,
        }
      }

      const urlParameters = `page=${page}`

      const response = await FeedAPI.getComments(postId, urlParameters, config)

      const comments = response.data.results
      const nextPage = response.data.next

      return {
        comments,
        nextPage,
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
