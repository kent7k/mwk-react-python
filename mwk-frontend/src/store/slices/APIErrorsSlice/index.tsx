import { createSlice } from '@reduxjs/toolkit'

export const APIErrorsSlice = createSlice({
  name: 'APIErrorsSlice',
  initialState: {
    APIErrors: [],
  },
  reducers: {
    /**
     * Set APIErrors
     * @param {Object} state
     * @param {Object} action
     */
    setAPIErrors(state, action) {
      return {
        ...state,
        APIErrors: action.payload.APIErrors,
      }
    },

    /**
     * Remove first element from APIErrors
     * @param {Object} state
     */
    shiftAPIErrors(state) {
      state.APIErrors.shift()
    },

    /**
     * Set APIErrors state to the []
     * @param {Object} state
     */
    clearAPIErrors(state) {
      return { ...state, APIErrors: [] }
    },
  },
})

export const { setAPIErrors, shiftAPIErrors, clearAPIErrors } =
  APIErrorsSlice.actions
export default APIErrorsSlice.reducer
