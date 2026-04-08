import http from './index.js'

/**
 * Fetch aggregated metrics for a given time range.
 * @param {number} days - Number of days to query (7, 30, 90)
 * @param {boolean} compare - Whether to include comparison data
 */
export function fetchMetrics(days, compare = false) {
  return http.get('/api/metrics', {
    params: { days, compare: compare ? 1 : undefined }
  }).then(res => res.data)
}

/**
 * Fetch hourly breakdown metrics.
 * @param {number} days - Number of days to query
 */
export function fetchHourlyMetrics(days) {
  return http.get('/api/metrics/hourly', {
    params: { days }
  }).then(res => res.data)
}
