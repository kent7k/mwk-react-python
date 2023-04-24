import API from '../../api/authentication'
import { debounce } from '../../lib'
import { removeToken } from '../slices/authentication/userSlice'

/**
 * Debounced function checkToken, send request to the API check token endpoint.
 */
export const checkToken = debounce((token, dispatch) => {
  const config = {
    headers: {
      Authorization: `Token ${token}`,
    },
  }

  API.checkToken(config).catch((error) => {
    if (error.response.status === 401) {
      dispatch(removeToken())
    }
  })
}, 1000)
