import { ref, onUnmounted } from 'vue'
import { createRealtimeConnection } from '../api/realtime.js'

/**
 * WebSocket lifecycle composable.
 * Provides reactive data stream and connection status.
 */
export function useWebSocket() {
  const data = ref(null)
  const status = ref('disconnected') // 'connecting' | 'connected' | 'disconnected'

  let connection = null

  function connect() {
    status.value = 'connecting'
    connection = createRealtimeConnection((message) => {
      status.value = 'connected'
      data.value = message
    })
  }

  function disconnect() {
    if (connection) {
      connection.disconnect()
      connection = null
    }
    status.value = 'disconnected'
    data.value = null
  }

  onUnmounted(() => {
    disconnect()
  })

  return {
    data,
    status,
    connect,
    disconnect
  }
}
