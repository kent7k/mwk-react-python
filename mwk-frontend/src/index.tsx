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
    // FIXME: The behavior of this code is incorrect in some scenarios.
    // When the user is not authenticated, they are redirected to the /login/ page.
    // When the user is authenticated, they are redirected to the /feed/ page.
    // However, there is currently an issue where the user can access the <Feed /> component
    // when authenticated, both at the '/' and '/feed/' routes. This behavior is unintended
    // and needs to be fixed.
    path: '/',
    component: <Feed />,
    protection: <AuthenticationProtectedRoute />,
  },
  {
    path: '/register/',
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
