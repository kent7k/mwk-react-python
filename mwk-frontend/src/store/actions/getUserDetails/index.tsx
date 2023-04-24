import { createAsyncThunk } from '@reduxjs/toolkit'

import AuthAPI from '../../../api/authentication'
import { setAPIErrors } from '../../slices/APIErrorsSlice'

export const getUserDetails = createAsyncThunk(
  'user/getUserDetails',
  async (_, { dispatch, rejectWithValue, getState }) => {
    try {
      const { user } = getState() as any

      const config = {
        headers: {
          Authorization: `Token ${user.token}`,
        },
      }

      const response = await AuthAPI.getUserDetails(config)

      const { first_name, last_name } = response.data.user
      const { avatar, id } = response.data

      return {
        profile_id: id,
        first_name,
        last_name,
        avatar,
      }
    } catch (err) {
      const APIErrors = [
        'Failed to retrieve your data. The server may be unavailable or your session may have expired. Please try again later!',
      ]

      dispatch(
        setAPIErrors({
          APIErrors,
        })
      )

      return rejectWithValue({
        error: 'Failed to get posts',
      })
    }
  }
)
