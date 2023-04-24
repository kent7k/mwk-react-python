import { createAsyncThunk } from '@reduxjs/toolkit'

import AuthAPI from '../../../api/authentication'
import { parseAPIAxiosErrors } from '../../../lib'
import { clearAPIErrors, setAPIErrors } from '../../slices/APIErrorsSlice'

export type LoginReturnType = {
  token: string
  userInfo: any
}

export const userLogin = createAsyncThunk<
  LoginReturnType, // 非同期関数の戻り値の型
  { username: string; password: string },
  {
    rejectValue: {
      APIErrors: string[]
    }
  }
>(
  'user/login',
  async ({ username, password }, { dispatch, rejectWithValue }) => {
    try {
      const response = await AuthAPI.login({ username, password })
      dispatch(clearAPIErrors())
      return {
        token: response.data.token,
        userInfo: response.data.user,
      }
    } catch (err) {
      const APIErrors = parseAPIAxiosErrors(err) as string[]

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
