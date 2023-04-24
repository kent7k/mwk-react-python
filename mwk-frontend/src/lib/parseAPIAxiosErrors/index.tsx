/**
 * Parse AxiosError nested object to the flat list of errors
 * @param {import('axios').AxiosError} err
 * @param {Number} recursionDepth
 * @returns {[String]}
 */
export function parseAPIAxiosErrors(err, recursionDepth = 10) {
  if (err.response && err.response.status === 0) {
    return ['The server is unavailable, please try again later.']
  }

  if (err.response) {
    const isInstanceOf = (object, type) => {
      const typeName = type.name
      const objectConstructor = Object.getPrototypeOf(object)
      const isObjectInstanceOfType = objectConstructor.name === typeName

      return isObjectInstanceOfType
    }

    const getErrorsArray = (initial_array, subEl) => {
      if (isInstanceOf(subEl, Object)) {
        return getErrorsArray(
          initial_array,
          Object.values(subEl)
            .flat(recursionDepth)
            .reduce((arr, el) => getErrorsArray(arr, el), [])
        )
      }

      return [...initial_array, subEl]
    }

    return Object.values(err.response.data)
      .flat(recursionDepth)
      .reduce((arr, el) => getErrorsArray(arr, el), [])
  }

  if (err.request) {
    return ['Something went wrong, we are already dealing with it.']
  }

  return [
    'Error! The programmer did something wrong, we are already dealing with it.',
  ]
}
