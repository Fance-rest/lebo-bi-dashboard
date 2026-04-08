<template>
  <span class="animated-number">{{ prefix }}{{ displayText }}{{ computedSuffix }}</span>
</template>

<script setup>
import { ref, watch, onUnmounted, computed } from 'vue'

const props = defineProps({
  value: {
    type: Number,
    required: true,
  },
  prefix: {
    type: String,
    default: '',
  },
  suffix: {
    type: String,
    default: '',
  },
  decimals: {
    type: Number,
    default: 0,
  },
  duration: {
    type: Number,
    default: 900,
  },
})

const displayValue = ref(props.value)
let rafId = null

function easeOutCubic(t) {
  return 1 - Math.pow(1 - t, 3)
}

function animateTo(from, to) {
  if (rafId) cancelAnimationFrame(rafId)
  const start = performance.now()
  const diff = to - from

  function step(now) {
    const elapsed = now - start
    const progress = Math.min(elapsed / props.duration, 1)
    displayValue.value = from + diff * easeOutCubic(progress)
    if (progress < 1) {
      rafId = requestAnimationFrame(step)
    } else {
      displayValue.value = to
      rafId = null
    }
  }

  rafId = requestAnimationFrame(step)
}

watch(
  () => props.value,
  (newVal, oldVal) => {
    animateTo(oldVal ?? 0, newVal)
  }
)

onUnmounted(() => {
  if (rafId) cancelAnimationFrame(rafId)
})

const useWan = computed(() => Math.abs(displayValue.value) >= 10000)

const displayText = computed(() => {
  if (useWan.value) {
    return (displayValue.value / 10000).toFixed(1)
  }
  return displayValue.value.toFixed(props.decimals)
})

const computedSuffix = computed(() => {
  const unit = useWan.value ? '万' : ''
  return unit + props.suffix
})
</script>

<style scoped>
.animated-number {
  font-variant-numeric: tabular-nums;
  font-size: inherit;
  color: inherit;
  white-space: nowrap;
}
</style>
