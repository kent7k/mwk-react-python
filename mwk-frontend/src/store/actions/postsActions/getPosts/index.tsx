import { createAsyncThunk } from '@reduxjs/toolkit'

import FeedAPI from '../../../../api/feed'
import { parseAPIAxiosErrors } from '../../../../lib'
import { urlParamEncode } from '../../../../lib/feed'
import { setAPIErrors } from '../../../slices/APIErrorsSlice'

export const getPosts = createAsyncThunk(
  'posts/getPosts',
  async (_: any, { rejectWithValue, dispatch, getState }) => {
    try {
      const { user, posts: postsState } = getState() as any
      const {
        nextPage: page,
        postsFilters: { priority, ordering, category },
      } = postsState

      if (!page) {
        return {
          posts: [],
          nextPage: null,
        }
      }

      const config = {
        headers: {
          Authorization: `Token ${user.token}`,
        },
      }

      const priorityParam = urlParamEncode(priority, 'on', priority)
      const orderingParam = urlParamEncode('ordering', ordering, ordering)
      const categoryParam = urlParamEncode('category', category, category)

      const urlParameters = `page=${page}${priorityParam}${orderingParam}${categoryParam}`

      const response = await FeedAPI.getPosts(urlParameters, config)
      const posts = response.data.results
      const nextPage = response.data.next

      return {
        posts,
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
