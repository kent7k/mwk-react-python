import React from 'react'
import { useDispatch, useSelector } from 'react-redux'

import Box from '@mui/material/Box'

import { useFormik } from 'formik'
import * as Yup from 'yup'

import { addComment } from '../../../../../store/actions/commentsActions/addComment'

import { AddPostCommentAvatar } from './AddPostCommentAvatar'
import { AddPostCommentBody } from './AddPostCommentBody'
import { AddPostCommentButton } from './AddPostCommentButton'

export const AddPostComment = ({ id, parent = null }) => {
  const { post } = useSelector((state: any) => state.posts)

  const dispatch: any = useDispatch()

  const validationSchema = Yup.object({
    body: Yup.string().required('You cannot leave a blank comment.'),
  })

  const formik = useFormik({
    initialValues: {
      body: '',
    },
    validationSchema,
    onSubmit: (values) => {
      dispatch(
        addComment({
          post: post.id,
          body: values.body,
          parent,
        })
      )
    },
  })

  return (
    <Box
      component="form"
      display="flex"
      px={3}
      py={1}
      noValidate
      autoComplete="off"
      flexDirection="column"
      onSubmit={formik.handleSubmit}
    >
      <Box sx={{ display: 'flex', alignItems: 'center', width: '100%' }}>
        <AddPostCommentAvatar />
        <AddPostCommentBody
          handleChange={formik.handleChange}
          value={formik.values.body}
          name="body"
          id={id}
          isError={formik.errors.body && formik.touched.body}
          helperText={
            formik.errors.body && formik.touched.body
              ? formik.errors.body
              : undefined
          }
        />
        <AddPostCommentButton />
      </Box>
    </Box>
  )
}
