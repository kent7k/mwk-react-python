import { createAsyncThunk } from '@reduxjs/toolkit'

import AuthAPI from '../../../api/authentication'
import { parseAPIAxiosErrors } from '../../../lib'

interface ActivateData {
  uid: string
  token: string
}

export const userActivate = createAsyncThunk(
  'user/activate',
  async (data: ActivateData, { rejectWithValue }) => {
    try {
      const { uid, token } = data
      await AuthAPI.activate(uid, token)
      return null
    } catch (err) {
      const APIErrors = parseAPIAxiosErrors(err)

      return rejectWithValue({
        APIErrors,
      })
    }
  }
)
