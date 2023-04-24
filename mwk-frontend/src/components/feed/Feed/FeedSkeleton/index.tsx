import React from 'react'

import Grid from '@mui/material/Grid'

import { PostCard } from '../../card'

export const FeedSkeleton = () => (
  <React.Fragment>
    {Array.from(Array(3)).map((_, idx) => (
      <Grid
        item
        // eslint-disable-next-line react/no-array-index-key
        key={idx}
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          width: '100%',
        }}
      >
        <PostCard
          maxWidth={500}
          loading
          avatarAlt=""
          avatarSrc=""
          title=""
          subheader=""
          images={[]}
          content=""
          timesince=""
          time=""
          likesCount={0}
          commentsCount={0}
          isLiked={false}
          viewsCount={0}
          id=""
        />
      </Grid>
    ))}
  </React.Fragment>
)
