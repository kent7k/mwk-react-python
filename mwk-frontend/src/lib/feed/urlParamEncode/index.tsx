/**
 * Encode url param, e.g condition ? &{name}={value} : ''
 * @param {String} name
 * @param {String} value
 * @param {boolean} condition
 * @returns {String}
 */
export const urlParamEncode = (name, value, condition) =>
  `${condition ? `&${name}=${value}` : ''}`
