import React from 'react'

import MoreVertIcon from '@mui/icons-material/MoreVert'
import Avatar from '@mui/material/Avatar'
import CardHeader from '@mui/material/CardHeader'
import IconButton from '@mui/material/IconButton'
import Link from '@mui/material/Link'
import Skeleton from '@mui/material/Skeleton'

type Props = {
  loading?: boolean
  avatarAlt: string
  avatarSrc: string
  href: string
  title: string
  subheader: string
}

export const PostCardHeader: React.FC<Props> = ({
  loading,
  avatarAlt,
  avatarSrc,
  href,
  title,
  subheader,
}) => {
  const getAvatar = () => {
    if (loading) {
      return (
        <Skeleton animation="wave" variant="circular" width={40} height={40} />
      )
    }
    return <Avatar alt={avatarAlt} src={avatarSrc} variant="circular" />
  }
  return (
    <CardHeader
      avatar={getAvatar()}
      action={
        <IconButton aria-label="settings">
          <MoreVertIcon />
        </IconButton>
      }
      title={
        loading ? (
          <Skeleton
            animation="wave"
            height={10}
            width="80%"
            style={{ marginBottom: 6 }}
          />
        ) : (
          <Link underline="none" href={href} variant="body2">
            {title}
          </Link>
        )
      }
      subheader={
        loading ? (
          <Skeleton animation="wave" height={10} width="40%" />
        ) : (
          subheader
        )
      }
    />
  )
}
