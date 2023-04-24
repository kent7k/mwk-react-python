import React from 'react'

import Backdrop from '@mui/material/Backdrop'
import Box from '@mui/material/Box'
import Container from '@mui/material/Container'
import Fade from '@mui/material/Fade'
import MUIModal from '@mui/material/Modal'

type Props = {
  open: boolean
  handleClose: () => void
  sx?: object
  children: React.ReactNode
}

export const Modal: React.FC<Props> = ({
  open,
  handleClose,
  sx = {},
  children,
}) => {
  const boxStyle = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    bgcolor: 'background.paper',
    p: 4,
    maxWidth: 1000,
    minWidth: 310,
    outline: 'none',
    borderRadius: '0.5rem',
    WebkitBoxShadow: '0 3px 7px rgba(0, 0, 0, 0.3)',
    MozBoxShadow: '0 3px 7px rgba(0, 0, 0, 0.3)',
    boxShadow: '0 3px 7px rgba(0, 0, 0, 0.3)',
    ...sx,
  }

  return (
    <MUIModal
      closeAfterTransition
      BackdropComponent={Backdrop}
      BackdropProps={{
        timeout: 500,
      }}
      open={open}
      onClose={handleClose}
    >
      <Fade in={open}>
        <Container
          sx={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
          component="main"
          maxWidth="xl"
        >
          <Box sx={boxStyle}>{children}</Box>
        </Container>
      </Fade>
    </MUIModal>
  )
}
