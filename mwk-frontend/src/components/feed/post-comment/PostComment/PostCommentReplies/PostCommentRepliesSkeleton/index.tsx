import React from 'react'

import { PostCommentSkeleton } from '../../PostCommentSkeleton'

export const PostCommentRepliesSkeleton = () => (
  <React.Fragment>
    {Array.from(Array(3)).map((_, idx) => (
      // eslint-disable-next-line react/no-array-index-key
      <div key={idx}>
        <PostCommentSkeleton />
      </div>
    ))}
  </React.Fragment>
)
