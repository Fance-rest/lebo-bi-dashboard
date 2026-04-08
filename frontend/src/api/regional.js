import http from './index.js'

/**
 * Fetch regional distribution data for the map chart.
 */
export function fetchRegionalData() {
  return http.get('/api/regional').then(res => res.data)
}
