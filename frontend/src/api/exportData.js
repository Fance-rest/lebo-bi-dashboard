/**
 * Trigger a CSV download via a temporary anchor element.
 * @param {string} type - Export type (e.g., 'metrics', 'brands', 'regional')
 * @param {number} days - Number of days to include
 */
export function downloadCSV(type, days) {
  const url = `/api/export/csv?type=${encodeURIComponent(type)}&days=${encodeURIComponent(days)}`
  const a = document.createElement('a')
  a.href = url
  a.download = `${type}_${days}d.csv`
  a.style.display = 'none'
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
}
