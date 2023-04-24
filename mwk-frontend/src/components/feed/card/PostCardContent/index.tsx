import React, { useState } from 'react'

import CardContent from '@mui/material/CardContent'
import Link from '@mui/material/Link'
import Typography from '@mui/material/Typography'

export const PostCardContent = ({ content }) => {
  const [isFullText, setIsFullText] = useState(false)

  const handleClick = () => {
    setIsFullText(true)
  }

  return (
    <CardContent>
      <Typography variant="body2">
        {!isFullText && content.length > 250 ? content.slice(0, 250) : content}
      </Typography>
      {isFullText || content.length < 250 ? null : (
        <Link underline="none" onClick={handleClick} variant="body2">
          Read more...
        </Link>
      )}
    </CardContent>
  )
}
