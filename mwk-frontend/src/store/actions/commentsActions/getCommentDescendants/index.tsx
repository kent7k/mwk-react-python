import { createAsyncThunk } from '@reduxjs/toolkit'

import FeedAPI from '../../../../api/feed'
import { parseAPIAxiosErrors } from '../../../../lib'
import { setAPIErrors } from '../../../slices/APIErrorsSlice'

export const getCommentDescendants = createAsyncThunk(
  'comments/getCommentDescendants',
  async (commentId: number, { rejectWithValue, dispatch, getState }) => {
    try {
      const { user, comments: commentsState } = getState() as any

      const config = {
        headers: {
          Authorization: `Token ${user.token}`,
        },
      }

      const { descendantsPage } = commentsState

      const page = descendantsPage[commentId]

      if (!page) {
        return {
          descendants: [],
          nextPage: null,
          commentId,
        }
      }

      const urlParameters = `page=${page}`

      const response = await FeedAPI.getCommentDescendants(
        commentId,
        config,
        urlParameters
      )

      const descendants = response.data.results
      const nextPage = response.data.next

      return {
        descendants,
        commentId,
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
        commentId,
      })
    }
  }
)
