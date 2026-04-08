<template>
  <div class="loading-spinner" :style="spinnerStyle">
    <div class="spinner-ring" :style="ringStyle"></div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  size: {
    type: Number,
    default: 32,
  },
})

const spinnerStyle = computed(() => ({
  width: `${props.size}px`,
  height: `${props.size}px`,
}))

const ringStyle = computed(() => ({
  width: `${props.size}px`,
  height: `${props.size}px`,
  borderWidth: `${Math.max(2, Math.round(props.size / 10))}px`,
}))
</script>

<style scoped>
.loading-spinner {
  display: flex;
  align-items: center;
  justify-content: center;
}

.spinner-ring {
  box-sizing: border-box;
  border-style: solid;
  border-color: var(--border-subtle);
  border-top-color: var(--text-secondary);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
