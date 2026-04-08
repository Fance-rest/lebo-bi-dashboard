import http from './index.js'

/**
 * Fetch top content rankings.
 * @param {number} limit - Number of items to return
 */
export function fetchTopContent(limit = 10) {
  return http.get('/api/content/top', {
    params: { limit }
  }).then(res => res.data)
}

/**
 * Fetch top device rankings.
 * @param {number} limit - Number of items to return
 */
export function fetchTopDevices(limit = 10) {
  return http.get('/api/devices/top', {
    params: { limit }
  }).then(res => res.data)
}
