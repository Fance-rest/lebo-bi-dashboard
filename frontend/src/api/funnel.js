import http from './index.js'

/**
 * Fetch conversion funnel data.
 */
export function fetchFunnel() {
  return http.get('/api/funnel').then(res => res.data)
}
