<template>
  <div class="metric-card-row">
    <MetricCard
      label="日活跃用户"
      :value="summary.dau ?? 0"
      color="blue"
      :change-pct="summary.dau_change_pct"
    />
    <MetricCard
      label="活跃设备"
      :value="summary.active_devices ?? 0"
      color="teal"
      :change-pct="summary.active_devices_change_pct"
    />
    <MetricCard
      label="投屏次数"
      :value="summary.cast_count ?? 0"
      color="amber"
      :change-pct="summary.cast_count_change_pct"
    />
    <MetricCard
      label="收入"
      :value="summary.revenue ?? 0"
      prefix="¥"
      :is-money="true"
      color="violet"
      :change-pct="summary.revenue_change_pct"
    />
  </div>
</template>

<script setup>
import MetricCard from './MetricCard.vue'

defineProps({
  summary: {
    type: Object,
    required: true,
    default: () => ({ dau: 0, active_devices: 0, cast_count: 0, revenue: 0 }),
  },
})
</script>

<style scoped>
.metric-card-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1px;
  background: var(--border-subtle);
  border-radius: var(--radius-md);
  overflow: hidden;
  margin-top: var(--space-5);
}

.metric-card-row > :deep(.metric-card) {
  background: var(--bg-surface);
}

@media (max-width: 900px) {
  .metric-card-row {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
