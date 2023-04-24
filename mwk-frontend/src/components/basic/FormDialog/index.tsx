import React from 'react'

import Button from '@mui/material/Button'
import Dialog from '@mui/material/Dialog'
import DialogActions from '@mui/material/DialogActions'
import DialogContent from '@mui/material/DialogContent'
import DialogTitle from '@mui/material/DialogTitle'

type FormDialogProps = {
  open: boolean
  handleClose: () => void
  children: React.ReactNode
}

export const FormDialog: React.FC<FormDialogProps> = ({
  open,
  handleClose,
  children,
}) => (
  <div>
    <Dialog open={open} onClose={handleClose}>
      <DialogTitle>Feed Filters</DialogTitle>
      <DialogContent>{children}</DialogContent>
      <DialogActions>
        <Button onClick={handleClose}>Close</Button>
      </DialogActions>
    </Dialog>
  </div>
)
