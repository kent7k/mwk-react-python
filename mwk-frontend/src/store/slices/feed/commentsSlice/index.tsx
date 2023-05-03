import { createSlice } from '@reduxjs/toolkit'

import { findComment, parsePageFromNextPage } from '../../../../lib/feed'
import { addComment } from '../../../actions/commentsActions/addComment'
import { commentLike } from '../../../actions/commentsActions/commentLike'
import { getCommentDescendants } from '../../../actions/commentsActions/getCommentDescendants'
import { getComments } from '../../../actions/commentsActions/getComments'

interface Comment {
  id: string
  text: string
}

interface CommentsState {
  likePendingComments: { [key: string]: boolean | null }
  postComments: Comment[]
  nextPage: number | null
  descendantsLoading: { [key: string]: boolean }
  commentsLoading: boolean | null
  descendantsPage: { [key: string]: number | null }
  addCommentLoading: boolean | null
}

export const commentsSlice = createSlice({
  name: 'commentsSlice',
  initialState: {
    likePendingComments: {},
    postComments: [],
    nextPage: 1,
    commentsLoading: null,
    descendantsPage: {},
    descendantsLoading: {},
    addCommentLoading: null,
  } as CommentsState,
  reducers: {},
  extraReducers: {
    // commentsLike
    [`${commentLike.pending}`](state, action) {
      const { arg: commentId } = action.meta
      return {
        ...state,
        likePendingComments: {
          ...state.likePendingComments,
          [commentId]: null,
        },
      }
    },

    [`${commentLike.fulfilled}`](state, action) {
      const { action: actionType, commentId } = action.payload

      const comment = findComment(state.postComments, commentId)

      const isAdd = actionType === 'add'

      const updatedLikePendingComments = { ...state.likePendingComments }
      delete updatedLikePendingComments[commentId]

      const updatedComment = {
        ...comment,
        is_user_liked_comment: isAdd,
        liked_count: comment.liked_count + (isAdd ? 1 : -1),
      }

      const updatedPostComments = state.postComments.map((c) =>
        c.id === commentId ? updatedComment : c
      )

      return {
        ...state,
        postComments: updatedPostComments,
        likePendingComments: updatedLikePendingComments,
      }
    },

    [`${commentLike.rejected}`](state, action) {
      const { id: commentId } = action.payload
      const newLikePendingComments = { ...state.likePendingComments }
      delete newLikePendingComments[commentId]
      return {
        ...state,
        likePendingComments: newLikePendingComments,
      }
    },

    // getComments
    [`${getComments.pending}`](state) {
      return {
        ...state,
        commentsLoading: true,
      }
    },

    [`${getComments.fulfilled}`](state, action) {
      const { comments, nextPage } = action.payload

      const page = nextPage ? parsePageFromNextPage(nextPage) : null

      const newState = {
        ...state,
        postComments: state.postComments.concat(comments),
        nextPage: page,
        commentsLoading: false,
      }
      return newState
    },

    [`${getCommentDescendants.pending}`](state, action) {
      const { arg: commentId } = action.meta

      const descendantsPage = { ...state.descendantsPage }
      if (!(commentId in descendantsPage)) {
        descendantsPage[commentId] = 1
      }

      const descendantsLoading = { ...state.descendantsLoading }
      descendantsLoading[commentId] = true

      return {
        ...state,
        descendantsPage,
        descendantsLoading,
      }
    },

    [`${getCommentDescendants.fulfilled}`](state, action) {
      const { descendants, commentId, nextPage } = action.payload

      const page = parsePageFromNextPage(nextPage)

      const postComments = [...state.postComments]
      const comment = findComment(postComments, commentId)

      if (descendants.length) {
        if (comment.replies.length <= 2) {
          comment.replies = descendants
        } else {
          comment.replies = comment.replies.concat(descendants)
        }
      }

      const descendantsPage = { ...state.descendantsPage }
      descendantsPage[commentId] = page

      const descendantsLoading = { ...state.descendantsLoading }
      delete descendantsLoading[commentId]

      return {
        ...state,
        postComments,
        descendantsPage,
        descendantsLoading,
      }
    },

    [`${getCommentDescendants.rejected}`](state, action) {
      const { commentId } = action.payload

      const descendantsLoading = { ...state.descendantsLoading }
      delete descendantsLoading[commentId]

      return {
        ...state,
        descendantsLoading,
      }
    },

    [`${addComment.pending}`](state) {
      return {
        ...state,
        addCommentLoading: true,
      }
    },

    [`${addComment.fulfilled}`](state, action) {
      const { comment, parent } = action.payload

      const postComments = [...state.postComments]

      if (!parent) {
        postComments.unshift(comment)
      } else {
        const rootComment = findComment(postComments, parent)
        if (rootComment) {
          rootComment.replies.unshift(comment)
        }
      }

      return {
        ...state,
        postComments,
        addCommentLoading: false,
      }
    },

    [`${addComment.rejected}`](state) {
      return {
        ...state,
        addCommentLoading: false,
      }
    },
  },
})

export default commentsSlice.reducer
