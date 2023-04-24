import React from 'react'

import { PostCommentSkeleton } from '../../PostComment/PostCommentSkeleton'

export const PostCommentsSkeleton = () => (
  <React.Fragment>
    {Array.from(Array(3)).map((_, idx) => (
      // eslint-disable-next-line react/no-array-index-key
      <li key={idx}>
        <PostCommentSkeleton />
      </li>
    ))}
  </React.Fragment>
)
