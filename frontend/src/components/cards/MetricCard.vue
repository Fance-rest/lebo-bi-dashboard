<template>
  <div class="metric-card">
    <span class="metric-label">{{ label }}</span>
    <div class="metric-value-row">
      <AnimatedNumber class="metric-value" :value="value" :prefix="prefix" :decimals="isMoney ? 2 : 0" />
      <span v-if="changePct != null" class="metric-change" :class="changeClass">
        <svg v-if="changePct >= 0" width="10" height="10" viewBox="0 0 10 10"><path d="M5 1 L9 6 L1 6 Z" fill="currentColor" /></svg>
        <svg v-else width="10" height="10" viewBox="0 0 10 10"><path d="M5 9 L9 4 L1 4 Z" fill="currentColor" /></svg>
        {{ Math.abs(changePct).toFixed(1) }}%
      </span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import AnimatedNumber from './AnimatedNumber.vue'

const props = defineProps({
  label: { type: String, required: true },
  value: { type: Number, required: true },
  prefix: { type: String, default: '' },
  isMoney: { type: Boolean, default: false },
  color: { type: String, default: 'blue' },
  changePct: { type: Number, default: undefined },
})

const changeClass = computed(() =>
  props.changePct != null && props.changePct >= 0 ? 'change-up' : 'change-down'
)
</script>

<style scoped>
.metric-card {
  padding: var(--space-5);
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.metric-label {
  font-size: var(--text-xs);
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.metric-value-row {
  display: flex;
  align-items: baseline;
  gap: var(--space-3);
}

.metric-value {
  font-family: var(--font-display);
  font-size: var(--text-2xl);
  font-weight: 600;
  color: var(--text-primary);
  font-variant-numeric: tabular-nums;
}

.metric-change {
  display: flex;
  align-items: center;
  gap: 2px;
  font-size: var(--text-xs);
  font-variant-numeric: tabular-nums;
}

.change-up { color: var(--color-teal); }
.change-down { color: var(--color-rose); }
</style>
