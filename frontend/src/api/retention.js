import http from './index.js'

/**
 * Fetch user retention cohort data.
 */
export function fetchRetention() {
  return http.get('/api/retention').then(res => res.data)
}
