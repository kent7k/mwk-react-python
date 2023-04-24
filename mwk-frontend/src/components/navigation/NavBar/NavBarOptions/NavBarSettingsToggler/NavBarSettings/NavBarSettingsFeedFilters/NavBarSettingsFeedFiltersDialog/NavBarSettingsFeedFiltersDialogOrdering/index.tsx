import React from 'react'
import { useDispatch, useSelector } from 'react-redux'

import InputLabel from '@mui/material/InputLabel'
import MenuItem from '@mui/material/MenuItem'
import OutlinedInput from '@mui/material/OutlinedInput'
import Select from '@mui/material/Select'

import { setPostsOrdering } from '../../../../../../../../../store/slices/feed/postsSlice'

export const NavBarSettingsFeedFiltersDialogOrdering = () => {
  const dispatch: any = useDispatch()

  const { ordering } = useSelector((state: any) => state.posts.postsFilters)

  const handleChangeOrdering = (event) => {
    dispatch(
      setPostsOrdering({
        ordering: event.target.value,
      })
    )
  }

  return (
    <React.Fragment>
      <InputLabel id="orderingSelectLabel">Order by</InputLabel>
      <Select
        value={ordering || ''}
        labelId="orderingSelectLabel"
        input={<OutlinedInput label="Order by" />}
        onChange={handleChangeOrdering}
      >
        <MenuItem value="-created_at">Sort by newest first</MenuItem>
        <MenuItem value="created_at">Sort by oldest first</MenuItem>
      </Select>
    </React.Fragment>
  )
}
