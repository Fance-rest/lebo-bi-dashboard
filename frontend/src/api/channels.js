import http from './index.js'

/**
 * Fetch channel distribution data.
 * @param {number} days - Number of days to query
 */
export function fetchChannels(days) {
  return http.get('/api/channels', {
    params: { days }
  }).then(res => res.data)
}
