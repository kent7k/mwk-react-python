import React from 'react'

import Grid from '@mui/material/Grid'

import { PostCard } from '../../card'

export const PostSkeleton = () => (
  <Grid
    item
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
)
