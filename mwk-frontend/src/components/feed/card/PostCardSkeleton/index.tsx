import React from 'react'

import CardContent from '@mui/material/CardContent'
import Skeleton from '@mui/material/Skeleton'

import { PostCardHeader as CardHeader } from '../PostCardHeader'

export const PostCardSkeleton = () => (
  <React.Fragment>
    <CardHeader
      loading
      avatarAlt="avatar"
      avatarSrc="avatar"
      href="href"
      title="title"
      subheader="subheader"
    />
    <Skeleton sx={{ height: 300 }} animation="wave" variant="rectangular" />
    <CardContent>
      <Skeleton animation="wave" height={10} style={{ marginBottom: 6 }} />
      <Skeleton animation="wave" height={10} width="80%" />
    </CardContent>
  </React.Fragment>
)
