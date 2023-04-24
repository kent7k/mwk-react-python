/**
 * Parse number of nextpage from link to the nextpage
 * @param {String} nextPageLink
 * @returns {Number}
 */
export const parsePageFromNextPage = (nextPageLink) => {
  if (!nextPageLink) {
    return null
  }

  return parseInt(
    nextPageLink
      .split('?')
      .find((el) => el.includes('page'))
      .split('=')[1],
    10 // 基数を10に指定する
  )
}
