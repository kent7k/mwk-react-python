import React, { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'

import InputLabel from '@mui/material/InputLabel'
import MenuItem from '@mui/material/MenuItem'
import OutlinedInput from '@mui/material/OutlinedInput'
import Select from '@mui/material/Select'

import { getCategories } from '../../../../../../../../../store/actions/postsActions/getCategories/index'
import { setPostsCategory } from '../../../../../../../../../store/slices/feed/postsSlice'

export const NavBarSettingsFeedFiltersDialogCategory = () => {
  const { categories } = useSelector((state: any) => state.posts)
  const { category } = useSelector((state: any) => state.posts.postsFilters)

  const dispatch: any = useDispatch()

  const handleChangeCategory = (e) => {
    const selectedCategory = e.target.value
    dispatch(
      setPostsCategory({
        category: selectedCategory,
      })
    )
  }

  useEffect(() => {
    dispatch(getCategories())
  }, [dispatch])

  return (
    <React.Fragment>
      <InputLabel id="categorySelectLabel">Category</InputLabel>
      <Select
        value={category || ''}
        labelId="categorySelectLabel"
        input={<OutlinedInput label="Category" />}
        onChange={handleChangeCategory}
        >
        {categories
          ? categories.map((_) => (
              <MenuItem key={category.id} value={_.id}>
                {_.title}
              </MenuItem>
            ))
          : null}
      </Select>
    </React.Fragment>
  )
}
