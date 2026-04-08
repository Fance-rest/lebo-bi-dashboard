<template>
  <header class="dash-header">
    <div class="header-content">
      <div class="header-left">
        <h1 class="header-title">投屏运营数据中心</h1>
        <p class="header-subtitle">Smart TV & Casting</p>
      </div>
      <div class="header-right">
        <span v-if="countdown >= 0" class="header-countdown">{{ countdown }}s</span>
        <span class="header-ws" :class="wsClass" :title="wsTitle">
          <span class="ws-dot"></span>
        </span>
        <span class="header-datetime">{{ formattedTime }}</span>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  wsStatus: { type: String, default: 'disconnected' },
  countdown: { type: Number, default: -1 },
})

const now = ref(new Date())
let timer = null

onMounted(() => {
  timer = setInterval(() => { now.value = new Date() }, 1000)
})
onUnmounted(() => { if (timer) clearInterval(timer) })

const pad = (n) => String(n).padStart(2, '0')
const formattedTime = computed(() => {
  const d = now.value
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`
})

const wsConnected = computed(() => props.wsStatus === 'connected')
const wsClass = computed(() => wsConnected.value ? 'ws-connected' : 'ws-disconnected')
const wsTitle = computed(() => wsConnected.value ? 'WebSocket 已连接' : 'WebSocket 已断开')
</script>

<style scoped>
.dash-header {
  padding: var(--space-6) 0 var(--space-5);
  border-bottom: 1px solid var(--border-subtle);
}

.header-content {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
}

.header-title {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: 2px;
}

.header-subtitle {
  font-size: var(--text-xs);
  color: var(--text-muted);
  letter-spacing: 1px;
  text-transform: uppercase;
  margin-top: 2px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: var(--space-4);
}

.header-datetime {
  font-family: var(--font-display);
  font-size: var(--text-sm);
  font-variant-numeric: tabular-nums;
  color: var(--text-secondary);
}

.header-ws {
  display: inline-flex;
  align-items: center;
}

.ws-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  transition: background-color 0.3s;
}

.ws-connected .ws-dot {
  background-color: var(--color-teal);
}

.ws-disconnected .ws-dot {
  background-color: var(--text-muted);
}

.header-countdown {
  font-size: var(--text-xs);
  color: var(--text-muted);
  font-variant-numeric: tabular-nums;
}
</style>
