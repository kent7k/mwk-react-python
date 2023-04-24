/**
 * Find comment by id in root comments and their replies. Return null if not comment finded.
 * @param {Array} comments
 * @param {Number} commentId
 * @returns {Object}
 */
export const findComment = (comments, commentId) => {
  const rootComment = comments.find(({ id }) => commentId === id)
  if (rootComment) {
    return rootComment
  }

  // eslint-disable-next-line no-restricted-syntax
  for (const root of comments) {
    const comment = root.replies.find(({ id }) => commentId === id)
    if (comment) return comment
  }

  return null
}
