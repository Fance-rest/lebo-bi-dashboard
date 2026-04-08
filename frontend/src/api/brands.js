import http from './index.js'

/**
 * Fetch device brand distribution data.
 */
export function fetchBrands() {
  return http.get('/api/brands').then(res => res.data)
}
