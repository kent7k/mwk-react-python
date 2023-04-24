import React from 'react'

import TextField from '@mui/material/TextField'

export const AddPostCommentBody = ({
  handleChange,
  value,
  name,
  id,
  isError,
  helperText,
}) => (
  <TextField
    id={id}
    label="What do you think about this post?"
    fullWidth
    value={value}
    name={name}
    onChange={handleChange}
    multiline
    error={isError}
    helperText={helperText}
    FormHelperTextProps={{ sx: { ml: 0 } }}
  />
)
