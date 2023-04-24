import { useEffect, useState } from 'react'
import { useSelector } from 'react-redux'

import useMediaQuery from '@mui/material/useMediaQuery'

/**
 * Get selected app theme
 * @returns {String}
 */
export function useSelectedTheme() {
  const { theme } = useSelector((state: any) => state.theme)
  const prefersDarkMode = useMediaQuery('(prefers-color-scheme: dark)')
  const systemTheme = prefersDarkMode ? 'dark' : 'light'

  const [selectedTheme, setSelectedTheme] = useState(theme || systemTheme)

  useEffect(() => {
    if (theme) {
      setSelectedTheme(theme)
    }
  }, [prefersDarkMode, theme])

  return selectedTheme
}
