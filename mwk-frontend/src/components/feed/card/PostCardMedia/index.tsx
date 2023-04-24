import React, { useState } from 'react'

import CardMedia from '@mui/material/CardMedia'

import { Modal } from '../../../basic/Modal'

import { PostCardMediaSlider as Slider } from './PostCardMediaSlider'

interface Props {
  images: string[]
}

export const PostCardMedia: React.FC<Props> = ({ images }) => {
  const [modalOpen, setModalOpen] = useState(false)
  const [modalImageTarget, setModalImageTarget] = useState(null)

  const handleModalOpen = (src) => {
    setModalOpen(true)
    setModalImageTarget(src)
  }

  const handleModalClose = () => {
    setModalOpen(false)
  }

  const imageList: { src: string; photo: string }[] = images.map((image) => ({
    src: image,
    photo: image,
  }))

  return images.length ? (
    <React.Fragment>
      <Slider handleModalOpen={handleModalOpen} images={imageList} />
      {modalOpen && modalImageTarget && (
        <Modal
          sx={{
            p: 1,
          }}
          open={modalOpen}
          handleClose={handleModalClose}
        >
          <CardMedia
            component="img"
            sx={{
              maxHeight: '500px',
            }}
            src={modalImageTarget}
            loading="lazy"
            alt=""
          />
        </Modal>
      )}
    </React.Fragment>
  ) : null
}
