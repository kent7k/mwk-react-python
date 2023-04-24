import { useEffect } from 'react'
import { useDispatch, useSelector } from 'react-redux'

import { getUserDetails } from '../../store/actions'

/**
 * Get user token and info
 * @returns {[String, Object]}
 */
export function useUser() {
  const dispatch: any = useDispatch()
  const { userInfo, token } = useSelector((state: any) => state.user)

  const all = (array, fn) => array.filter(fn).length === array.length

  useEffect(() => {
    if (all(Object.values(userInfo), (el) => el === null) && token) {
      // FIXME: if not userInfo
      dispatch(getUserDetails())
    }
  }, [dispatch, userInfo, token])

  return [token, userInfo]
}
