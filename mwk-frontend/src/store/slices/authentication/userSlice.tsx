import { createSlice } from '@reduxjs/toolkit'

import {
  getFromLocalStorage,
  removeFromLocalStorage,
  setToLocalStorage,
} from '../../../lib'
import {
  getUserDetails,
  userActivate,
  userLogin,
  userLogout,
  userRegister,
} from '../../actions'

const userToken = getFromLocalStorage('userToken')

interface UserState {
  userInfo: {
    profile_id: number | null
    first_name: string | null
    last_name: string | null
    avatar: string | null
  }
  token: string | null
  loading: boolean | null
  success: boolean | null
  errors: any[]
  countries: any[]
  cities: any[]
  rejected: boolean | null
}

const initialState: UserState = {
  userInfo: {
    profile_id: null,
    first_name: null,
    last_name: null,
    avatar: null,
  },
  token: userToken,
  loading: null,
  success: null,
  errors: [],
  countries: [],
  cities: [],
  rejected: null,
}

const userSlice = createSlice({
  name: 'userSlice',
  initialState,
  reducers: {
    /**
     * Set success state to the null
     * @param {Object} state
     */
    clearSuccess(state) {
      return {
        ...state,
        success: initialState.success,
      }
    },

    /**
     * Set cities state to the []
     * @param {Object} state
     */
    clearCities(state) {
      return {
        ...state,
        cities: [],
      }
    },

    /**
     * Remove token from ls and set token state to the null
     * @param {Object} state
     */
    removeToken(state) {
      removeFromLocalStorage('userToken')
      return {
        ...state,
        token: null,
      }
    },
  },
  extraReducers: {
    // userRegister
    [`${userRegister.pending}`](state) {
      return {
        ...state,
        success: false,
        loading: true,
      }
    },

    [`${userRegister.fulfilled}`](state) {
      return {
        ...state,
        success: true,
        loading: false,
      }
    },

    [`${userRegister.rejected}`](state) {
      return {
        ...state,
        loading: false,
      }
    },

    // userLogin
    [`${userLogin.pending}`](state) {
      return {
        ...state,
        loading: true,
      }
    },

    [`${userLogin.fulfilled}`](state, action) {
      setToLocalStorage('userToken', action.payload.token)
      return {
        ...state,
        loading: false,
        token: action.payload.token,
        userInfo: action.payload.userInfo,
      }
    },

    [`${userLogin.rejected}`](state) {
      return {
        ...state,
        loading: false,
      }
    },

    // userLogout
    [`${userLogout.pending}`](state) {
      return {
        ...state,
        loading: true,
      }
    },

    [`${userLogout.fulfilled}`](state) {
      const newState = {
        ...state,
        loading: false,
        userInfo: initialState.userInfo,
        token: null,
      }
      removeFromLocalStorage('userToken')
      return newState
    },

    [`${userLogout.rejected}`](state) {
      return {
        ...state,
        loading: false,
      }
    },

    // userActivate
    [`${userActivate.pending}`](state) {
      return {
        ...state,
        success: false,
        loading: true,
      }
    },

    [`${userActivate.fulfilled}`](state) {
      return {
        ...state,
        loading: false,
        success: true,
      }
    },

    [`${userActivate.rejected}`](state, action) {
      return {
        ...state,
        loading: false,
        rejected: true,
        errors: action.payload.APIErrors,
      }
    },

    // getUserDetails
    [`${getUserDetails.pending}`](state) {
      return {
        ...state,
        loading: true,
      }
    },

    [`${getUserDetails.fulfilled}`](state, action) {
      return {
        ...state,
        userInfo: action.payload,
        loading: false,
      }
    },

    [`${getUserDetails.rejected}`](state) {
      return {
        ...state,
        loading: false,
      }
    },
  },
})

export const { clearSuccess, removeToken } =
  userSlice.actions
export default userSlice.reducer
