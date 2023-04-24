import { createAsyncThunk } from '@reduxjs/toolkit'

import AuthAPI from '../../../api/authentication'
import { parseAPIAxiosErrors } from '../../../lib'
import { setAPIErrors } from '../../slices/APIErrorsSlice'

export const userLogout = createAsyncThunk(
  'user/logout',
  async (_, { dispatch, rejectWithValue, getState }) => {
    try {
      // FIXME: type RootState
      const { user } = getState() as any

      const config = {
        headers: {
          Authorization: `Token ${user.token}`,
        },
      }

      await AuthAPI.logout(config)

      return null
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
