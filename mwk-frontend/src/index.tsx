import { StrictMode, Suspense, useMemo } from 'react'
import { Provider as ReduxProvider } from 'react-redux'

import CssBaseline from '@mui/material/CssBaseline'
import { ThemeProvider, createTheme } from '@mui/material/styles'

import ReactDOM from 'react-dom/client'

import { Activation, Login, Logout, Register } from './components'
import { Feed } from './components/feed/Feed'
import { Post } from './components/feed/post/Post'
import { Page404 } from './components/pages/Page404'
import { AnonymousProtectedRoute } from './components/routing/AnonymousProtectedRoute'
import { AuthenticationProtectedRoute } from './components/routing/AuthenticationProtectedRoute'
import { useSelectedTheme } from './hooks'
import Router from './router'
import reduxStore from './store'

import './index.css'

const routes = [
  {
    path: '/not-found/',
    component: <Page404 />,
  },
  {
    path: '/',
    component: <Register />,
    protection: <AnonymousProtectedRoute />,
  },
  {
    path: '/login/',
    component: <Login />,
    protection: <AnonymousProtectedRoute />,
  },
  {
    path: '/logout/',
    component: <Logout />,
    protection: <AuthenticationProtectedRoute />,
  },
  {
    path: '/activate/:uid/:token/',
    component: <Activation />,
    protection: <AnonymousProtectedRoute />,
  },
  {
    path: '/feed/',
    component: <Feed />,
    protection: <AuthenticationProtectedRoute />,
  },
  {
    path: '/feed/:postId/',
    component: <Post />,
    protection: <AuthenticationProtectedRoute />,
  },
]

export const App = () => {
  const themeMode = useSelectedTheme()

  const theme = useMemo(
    () =>
      createTheme({
        palette: {
          mode: themeMode,
          ...(themeMode === 'dark'
            ? {
                primary: {
                  main: '#3f51b5',
                },
                secondary: {
                  main: '#f50057',
                },
              }
            : {}),
        },
      }),
    [themeMode]
  )

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline>
        <Router routes={routes} />
      </CssBaseline>
    </ThemeProvider>
  )
}

const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement)

root.render(
  <StrictMode>
    <ReduxProvider store={reduxStore}>
      <Suspense fallback={<div>Loading</div>}>
        <App />
      </Suspense>
    </ReduxProvider>
  </StrictMode>
)
