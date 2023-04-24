import { createSlice } from '@reduxjs/toolkit'

import { getFromLocalStorage, setToLocalStorage } from '../../../lib'

const theme = getFromLocalStorage('selectedTheme')

export const themeSlice = createSlice({
  name: 'themeSlice',
  initialState: {
    theme,
  },
  reducers: {
    /**
     * Set theme to the ls and state
     * @param {Object} state
     * @param {Object} action
     */
    setTheme(state, action) {
      setToLocalStorage('selectedTheme', action.payload.theme)
      return { ...state, theme: action.payload.theme }
    },
  },
})

export const { setTheme } = themeSlice.actions
export default themeSlice.reducer
