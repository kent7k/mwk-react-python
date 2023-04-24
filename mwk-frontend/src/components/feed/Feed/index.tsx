import React, { useCallback, useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'

import { getPostsWrapper } from '../../../store/actions/postsActions/getPostsWrapper/index'
import { FeedInfiniteScroll } from '../FeedInfiniteScroll'

import { FeedCards } from './FeedCards'
import { FeedContainer } from './FeedContainer'
import { FeedErrors } from './FeedErrors'

export const Feed = () => {
  const dispatch: any = useDispatch()
  const { rejected, postsFilters, posts } = useSelector(
    (state: any) => state.posts
  )

  const fetchPosts = useCallback(() => {
    dispatch(getPostsWrapper())
  }, [dispatch])

  useEffect(() => {
    document.title = 'Feed || App'
  }, [])

  useEffect(() => {
    fetchPosts()
  }, [fetchPosts, postsFilters])

  return (
    <FeedContainer>
      <FeedErrors />
      <FeedCards />
      {rejected || !posts.length ? null : (
        <FeedInfiniteScroll onIntersecting={fetchPosts} />
      )}
    </FeedContainer>
  )
}
