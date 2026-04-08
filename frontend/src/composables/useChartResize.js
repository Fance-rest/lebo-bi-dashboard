import { onUnmounted, watch } from 'vue'

/**
 * Handles ECharts instance resizing via ResizeObserver.
 * Automatically disposes the chart on unmount.
 * @param {import('vue').Ref} chartRef - Ref to the ECharts instance
 * @param {import('vue').Ref} containerRef - Ref to the container DOM element
 */
export function useChartResize(chartRef, containerRef) {
  let observer = null

  function setupObserver() {
    if (!containerRef.value) return

    observer = new ResizeObserver(() => {
      if (chartRef.value) {
        chartRef.value.resize()
      }
    })
    observer.observe(containerRef.value)
  }

  // Watch for container becoming available
  watch(containerRef, (el) => {
    if (observer) {
      observer.disconnect()
    }
    if (el) {
      setupObserver()
    }
  }, { immediate: true })

  onUnmounted(() => {
    if (observer) {
      observer.disconnect()
      observer = null
    }
    if (chartRef.value) {
      chartRef.value.dispose()
      chartRef.value = null
    }
  })
}
