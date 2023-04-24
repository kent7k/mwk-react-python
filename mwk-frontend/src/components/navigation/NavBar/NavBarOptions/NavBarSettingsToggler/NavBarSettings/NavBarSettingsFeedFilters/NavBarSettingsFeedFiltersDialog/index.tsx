import React from 'react'

import FormControl from '@mui/material/FormControl'
import Stack from '@mui/material/Stack'

import { FormDialog } from '../../../../../../../basic/FormDialog'

import { NavBarSettingsFeedFiltersDialogCategory } from './NavBarSettingsFeedFiltersDialogCategory'
import { NavBarSettingsFeedFiltersDialogOrdering } from './NavBarSettingsFeedFiltersDialogOrdering'
import { NavBarSettingsFeedFiltersDialogPriority } from './NavBarSettingsFeedFiltersDialogPriority'

type Props = {
  open: boolean
  handleClose: () => void
}

export const NavBarSettingsFeedFiltersDialog: React.FC<Props> = ({
  open,
  handleClose,
}) => (
  <FormDialog open={open} handleClose={handleClose}>
    <Stack spacing={1} sx={{ display: 'flex', flexWrap: 'wrap' }}>
      <div>
        <FormControl>
          <NavBarSettingsFeedFiltersDialogPriority />
        </FormControl>
      </div>
      <div>
        <FormControl fullWidth>
          <NavBarSettingsFeedFiltersDialogOrdering />
        </FormControl>
      </div>
      <div>
        <FormControl fullWidth>
          <NavBarSettingsFeedFiltersDialogCategory />
        </FormControl>
      </div>
    </Stack>
  </FormDialog>
)
