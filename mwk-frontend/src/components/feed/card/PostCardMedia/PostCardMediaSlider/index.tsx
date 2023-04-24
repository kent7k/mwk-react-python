import React from 'react'

import CardMedia from '@mui/material/CardMedia'

import { Lazy } from 'swiper'
import { Swiper, SwiperSlide } from 'swiper/react'
// import 'swiper/css'
// import 'swiper/css/lazy'

interface Photo {
  photo: string
}

type Props = {
  images: Photo[]
  handleModalOpen: (src: string) => void
}

export const PostCardMediaSlider: React.FC<Props> = ({
  images,
  handleModalOpen,
}) => (
  <Swiper spaceBetween={50} modules={[Lazy]} slidesPerView={1} autoHeight lazy>
    {images.map((img) => (
      <SwiperSlide key={img.photo}>
        <CardMedia
          component="img"
          sx={{
            maxHeight: '300px',
          }}
          onClick={() => handleModalOpen(img.photo)}
          className="swiper-lazy"
          data-src={img.photo}
          alt=""
        />
      </SwiperSlide>
    ))}
  </Swiper>
)
