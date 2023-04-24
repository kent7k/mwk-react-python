import { createAsyncThunk } from '@reduxjs/toolkit'

import API from '../../../api/authentication'
import { parseAPIAxiosErrors } from '../../../lib'
import { clearAPIErrors, setAPIErrors } from '../../slices/APIErrorsSlice'

export const userRegister = createAsyncThunk(
  'user/register',
  async (userData: any, { dispatch, rejectWithValue }) => {
    try {
      await API.register(userData)
      dispatch(clearAPIErrors())
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
