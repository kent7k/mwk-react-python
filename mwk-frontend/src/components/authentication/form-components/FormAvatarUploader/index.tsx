import React, { useState } from 'react'

import CloudUploadIcon from '@mui/icons-material/CloudUpload'
import Avatar from '@mui/material/Avatar'
import Box from '@mui/material/Box'
import Button from '@mui/material/Button'
import Card from '@mui/material/Card'
import Stack from '@mui/material/Stack'
import Typography from '@mui/material/Typography'

import { showComponent } from '../../../../lib'

type Props = {
  id: string
  name: string
  width?: number
  height?: number
  helperText: string
  handleChange: (data: string, isValid?: boolean) => void
  setError?: (field: string, error: string) => void
}

export const FormAvatarUploader: React.FC<Props> = ({
  id,
  name,
  width,
  height,
  helperText,
  handleChange,
  setError,
}) => {
  const [avatarPreview, setAvatarPreview] = useState('default')

  const handleFileChange = (e) => {
    const fileReader = new FileReader()
    const file = e.target.files[0]
    const allowedTypes = ['image/jpeg', 'image/png', 'image/jpg', 'image/gif']

    fileReader.onload = () => {
      if (fileReader.readyState === 2) {
        // FIXME
        setAvatarPreview(String(fileReader.result))
        handleChange(String(fileReader.result))
      }
    }

    if (file) {
      if (allowedTypes.indexOf(file.type) !== -1) {
        fileReader.readAsDataURL(file)
      } else {
        handleChange('', false)
        if (setError) {
          setError(
            name,
            'The file you uploaded is either corrupted or not an image.'
          )
        }
        setAvatarPreview('default')
      }
    } else {
      handleChange('')
      setAvatarPreview('default')
    }
  }

  return (
    <Card>
      {showComponent(
        <Typography
          sx={{
            paddingTop: '7px',
            color: '#f44336',
            fontWeight: 400,
            fontSize: '0.75rem',
          }}
          align="center"
          variant="caption"
          display="block"
        >
          {helperText}
        </Typography>,
        helperText
      )}
      <Box p={2}>
        <Stack justifyContent="center" alignItems="center" spacing={2}>
          <Avatar
            src={avatarPreview}
            sx={{
              width,
              height,
            }}
          />
          <Button
            component="label"
            startIcon={<CloudUploadIcon />}
            variant="contained"
          >
            Upload Profile Photo
            <input
              accept="image/*"
              type="file"
              id={id}
              name={name}
              hidden
              onChange={handleFileChange}
            />
          </Button>
        </Stack>
      </Box>
    </Card>
  )
}
