import moment from 'moment'

/**
 * Get timesince and time from created_at string
 * @param {String} created_at
 * @returns {[String, String]}
 */
export function getTimeInfo(created_at): any {
  const timesince = moment(Date.parse(created_at)).fromNow()
  const createdAtDate = new Date(created_at)

  const time = `${createdAtDate
    .getHours()
    .toString()
    .padStart(2, '0')}:${createdAtDate
    .getMinutes()
    .toString()
    .padStart(2, '0')}`
  return [timesince, time]
}
