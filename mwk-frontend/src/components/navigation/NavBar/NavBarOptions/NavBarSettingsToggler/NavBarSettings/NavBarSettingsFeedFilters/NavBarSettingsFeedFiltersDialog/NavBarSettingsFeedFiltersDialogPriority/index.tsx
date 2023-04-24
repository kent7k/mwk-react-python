import React from 'react'
import { useDispatch, useSelector } from 'react-redux'

import FormControlLabel from '@mui/material/FormControlLabel'
import FormLabel from '@mui/material/FormLabel'
import Radio from '@mui/material/Radio'
import RadioGroup from '@mui/material/RadioGroup'

import { setPostsPriority } from '../../../../../../../../../store/slices/feed/postsSlice'

export const NavBarSettingsFeedFiltersDialogPriority = () => {
  const { priority } = useSelector((state: any) => state.posts.postsFilters)
  const dispatch: any = useDispatch()

  const handleChangePriority = (event) => {
    dispatch(
      setPostsPriority({
        priority: event.target.value,
      })
    )
  }

  return (
    <React.Fragment>
      <FormLabel
        sx={{
          mb: 0.5,
          '&.Mui-focused': {},
        }}
        id="feed_filters_label"
      >
        Post priority
      </FormLabel>
      <RadioGroup
        aria-labelledby="feed_filters_label"
        name="posts_priority"
        value={priority}
        onChange={handleChangePriority}
      >
        <FormControlLabel
          value="is_interesting"
          control={<Radio />}
          label="Show interesting first"
        />
        <FormControlLabel
          value="is_popular"
          control={<Radio />}
          label="Show popular first"
        />
      </RadioGroup>
    </React.Fragment>
  )
}
