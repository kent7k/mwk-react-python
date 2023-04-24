import React, { useEffect, useRef } from 'react'

import Typed from 'typed.js'

export const Page404 = () => {
  const typedElement = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const typed = new Typed(typedElement.current as Element, {
      strings: [
        'Oops!^1000 Looks like you got lost!!. <br /> ^1000' +
          'Sorry. <br /> ^1000' +
          'The page you requested <strong>does not exist.</strong> <br /> ^1000',
      ],
      typeSpeed: 20,
      showCursor: false,
    })

    // Destroying
    return () => {
      typed.destroy()
    }
  })

  return (
    <div
      className="page404Container"
      style={{
        color: '#fff',
      }}
    >
      <div className="page404Content">
        <div className="page404BrowserBar">
          <div className="page404BrowserBarIcons">
            <span className="page404Close page404Button" />
            <span className="page404Min page404Button" />
            <span className="page404Max page404Button" />
          </div>
          <p className="page404BrowserBarTitle">404.txt</p>
        </div>
        <div className="page-404__text" ref={typedElement} />
      </div>
    </div>
  )
}
