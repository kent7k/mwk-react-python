import { createSlice } from '@reduxjs/toolkit'

import { parsePageFromNextPage } from '../../../../lib/feed'
import { getCategories } from '../../../actions/postsActions/getCategories'
import { getPost } from '../../../actions/postsActions/getPost/index'
import { getPosts } from '../../../actions/postsActions/getPosts/index'
import { postLike } from '../../../actions/postsActions/postLike/index'

export const postsSlice = createSlice({
  name: 'postsSlice',
  initialState: {
    posts: [],
    nextPage: 1,
    loading: null,
    rejected: null,
    likePendingPosts: {},
    postsFilters: {
      priority: null,
      ordering: null,
      category: '',
    },
    post: null,
    postNotFound: null,
    categories: [],
  },

  reducers: {
    /**
     * Set postsFilters.priority
     * @param {Object} state
     * @param {Object} action
     */
    setPostsPriority(state: any, action: any) {
      const { priority } = action.payload

      if (state.postsFilters.priority !== priority) {
        // refresh
        return {
          ...state,
          posts: [],
          nextPage: 1,
          postsFilters: {
            ...state.postsFilters,
            priority,
          },
        }
      }

      return {
        ...state,
        postsFilters: {
          ...state.postsFilters,
          priority,
        },
      }
    },

    /**
     * Set postsFilters.ordering
     * @param {Object} state
     * @param {Object} action
     */
    setPostsOrdering(state, action) {
      const { ordering } = action.payload

      if (state.postsFilters.ordering !== ordering) {
        // refresh
        return {
          ...state,
          posts: [],
          nextPage: 1,
          postsFilters: {
            ...state.postsFilters,
            ordering,
          },
        }
      }

      return {
        ...state,
        postsFilters: {
          ...state.postsFilters,
          ordering,
        },
      }
    },

    /**
     * Set postsFilters.category
     * @param {Object} state
     * @param {Object} action
     */
    setPostsCategory(state, action) {
      const { category } = action.payload

      if (state.postsFilters.category !== category) {
        // refresh
        return {
          ...state,
          posts: [],
          nextPage: 1,
          postsFilters: {
            ...state.postsFilters,
            category,
          },
        }
      }

      return {
        ...state,
        postsFilters: {
          ...state.postsFilters,
          category,
        },
      }
    },
  },

  extraReducers: {
    // getPosts
    [`${getPosts.pending}`](state) {
      return {
        ...state,
        post: null,
        loading: true,
        rejected: false,
      }
    },

    [`${getPosts.fulfilled}`](state, action) {
      const { posts, nextPage } = action.payload

      const page = nextPage ? parsePageFromNextPage(nextPage) : null

      const newState = {
        ...state,
        posts: state.posts.concat(posts),
        nextPage: page,
        loading: false,
      }
      return newState
    },

    [`${getPosts.rejected}`](state) {
      return {
        ...state,
        loading: false,
        rejected: true,
      }
    },

    [`${getCategories.fulfilled}`](state, action) {
      const { categories } = action.payload

      return {
        ...state,
        categories,
      }
    },

    // postLike
    [`${postLike.pending}`](state, action) {
      const { arg: postId } = action.meta
      return {
        ...state,
        likePendingPosts: {
          ...state.likePendingPosts,
          [postId]: null,
        },
      }
    },

    [`${postLike.fulfilled}`](state, action) {
      const { action: actionType, postId } = action.payload

      const postInPosts = state.posts.find(({ id }) => postId === id)
      const post =
        state.post && state.post.id === postId ? state.post : postInPosts || {}

      const isAdd = actionType === 'add'

      const likePendingPosts = { ...state.likePendingPosts }
      delete likePendingPosts[postId]

      const updatedPost = {
        ...post,
        is_user_liked_post: isAdd,
        liked_count: post.liked_count + (isAdd ? 1 : -1),
      }

      const posts = state.posts.map((p) => (p.id === postId ? updatedPost : p))

      const updatedState = {
        ...state,
        posts,
        post: post.id === postId ? updatedPost : state.post,
        likePendingPosts,
      }

      return updatedState
    },

    [`${postLike.rejected}`](state, action) {
      const { id: postId } = action.payload
      const likePendingPosts = { ...state.likePendingPosts }
      delete likePendingPosts[postId]
      return { ...state, likePendingPosts }
    },

    // getPost

    [`${getPost.pending}`](state) {
      return {
        ...state,
        post: null,
        postNotFound: null,
        postComments: null,
        loading: true,
      }
    },

    [`${getPost.fulfilled}`](state, action) {
      const { post } = action.payload

      return {
        ...state,
        post,
        loading: false,
      }
    },

    [`${getPost.rejected}`](state, action) {
      const { status } = action.payload

      return {
        ...state,
        loading: false,
        postNotFound: status === 404,
      }
    },
  },
})

export const { setPostsPriority, setPostsOrdering, setPostsCategory } =
  postsSlice.actions

export default postsSlice.reducer
