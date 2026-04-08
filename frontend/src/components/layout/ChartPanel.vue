<template>
  <div class="chart-panel">
    <div v-if="title" class="panel-header">
      <h3 class="panel-title">{{ title }}</h3>
    </div>
    <div class="panel-body">
      <transition name="fade">
        <div v-if="loading" class="panel-loading">
          <LoadingSpinner :size="24" />
        </div>
      </transition>
      <div class="panel-content">
        <slot />
      </div>
    </div>
  </div>
</template>

<script setup>
import LoadingSpinner from '@/components/common/LoadingSpinner.vue'

defineProps({
  title: { type: String, default: '' },
  loading: { type: Boolean, default: false },
})
</script>

<style scoped>
.chart-panel {
  background: var(--bg-surface);
  border-radius: var(--radius-md);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.panel-header {
  padding: var(--space-4) var(--space-5) var(--space-2);
}

.panel-title {
  font-family: var(--font-body);
  font-size: var(--text-sm);
  font-weight: 500;
  color: var(--text-secondary);
  letter-spacing: 0.3px;
}

.panel-body {
  position: relative;
  flex: 1;
  min-height: 0;
}

.panel-content {
  width: 100%;
  height: 100%;
}

.panel-loading {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: oklch(13% 0.01 260 / 70%);
  z-index: 5;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
