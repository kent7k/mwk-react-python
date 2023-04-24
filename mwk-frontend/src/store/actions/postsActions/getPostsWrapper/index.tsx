import { createAsyncThunk } from '@reduxjs/toolkit'

import { getPosts } from '../getPosts'

export const getPostsWrapper = createAsyncThunk(
  'posts/getPostsWrapper',
  async (arg, { dispatch, getState }) => {
    const { loading } = (getState() as any).posts

    if (!loading) {
      dispatch(getPosts(arg))
    }
  }
)
