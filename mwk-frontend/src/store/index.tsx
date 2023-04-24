import { configureStore } from '@reduxjs/toolkit'

import { logoutMiddleware } from './middlewares'
import APIErrorsSlice from './slices/APIErrorsSlice'
import userSlice from './slices/authentication/userSlice'
import commentsSlice from './slices/feed/commentsSlice'
import postsSlice from './slices/feed/postsSlice'
import themeSlice from './slices/themeSlice'

export default configureStore({
  reducer: {
    APIErrors: APIErrorsSlice,
    user: userSlice,
    posts: postsSlice,
    comments: commentsSlice,
    theme: themeSlice,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware().concat(logoutMiddleware),
})
