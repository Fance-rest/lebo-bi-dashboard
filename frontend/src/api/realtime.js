/**
 * WebSocket manager for real-time data streaming.
 * Auto-reconnects with exponential backoff (max 5 retries).
 */

let ws = null
let retryCount = 0
let retryTimer = null
const MAX_RETRIES = 5

/**
 * Connect to the realtime WebSocket endpoint.
 * @param {Function} onMessage - Callback invoked with parsed message data
 * @returns {{ disconnect: Function }}
 */
export function createRealtimeConnection(onMessage) {
  function connect() {
    const protocol = location.protocol === 'https:' ? 'wss:' : 'ws:'
    const url = `${protocol}//${location.host}/ws/realtime`

    ws = new WebSocket(url)

    ws.onopen = () => {
      retryCount = 0
      console.log('[WS] Connected to realtime stream')
    }

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        onMessage(data)
      } catch (e) {
        console.error('[WS] Failed to parse message:', e)
      }
    }

    ws.onclose = (event) => {
      console.log('[WS] Connection closed', event.code)
      if (retryCount < MAX_RETRIES) {
        const delay = Math.min(1000 * Math.pow(2, retryCount), 30000)
        retryCount++
        console.log(`[WS] Reconnecting in ${delay}ms (attempt ${retryCount}/${MAX_RETRIES})`)
        retryTimer = setTimeout(connect, delay)
      }
    }

    ws.onerror = (error) => {
      console.error('[WS] Error:', error)
    }
  }

  function disconnect() {
    clearTimeout(retryTimer)
    retryCount = MAX_RETRIES // Prevent auto-reconnect
    if (ws) {
      ws.close()
      ws = null
    }
  }

  connect()

  return { disconnect }
}
