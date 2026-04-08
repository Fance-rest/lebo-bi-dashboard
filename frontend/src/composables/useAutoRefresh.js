import { ref, onUnmounted } from 'vue'

/**
 * Auto-refresh composable with countdown timer.
 * @param {Function} callback - Function to call on each tick
 * @param {number} defaultInterval - Default interval in seconds (default: 60)
 */
export function useAutoRefresh(callback, defaultInterval = 60) {
  const isActive = ref(false)
  const interval = ref(defaultInterval)
  const countdown = ref(defaultInterval)

  let refreshTimer = null
  let countdownTimer = null

  function start() {
    stop() // Clear any existing timers
    isActive.value = true
    countdown.value = interval.value

    // Countdown ticker (every 1s)
    countdownTimer = setInterval(() => {
      countdown.value--
      if (countdown.value <= 0) {
        countdown.value = interval.value
      }
    }, 1000)

    // Main refresh timer
    refreshTimer = setInterval(() => {
      callback()
      countdown.value = interval.value
    }, interval.value * 1000)
  }

  function stop() {
    isActive.value = false
    clearInterval(refreshTimer)
    clearInterval(countdownTimer)
    refreshTimer = null
    countdownTimer = null
    countdown.value = interval.value
  }

  onUnmounted(() => {
    stop()
  })

  return {
    isActive,
    interval,
    countdown,
    start,
    stop
  }
}
