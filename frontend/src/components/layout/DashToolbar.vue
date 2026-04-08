<template>
  <div class="dash-toolbar">
    <div class="toolbar-group">
      <button
        v-for="opt in dayOptions"
        :key="opt.value"
        class="tb-btn"
        :class="{ active: days === opt.value }"
        @click="emit('update:days', opt.value)"
      >{{ opt.label }}</button>
    </div>

    <div class="toolbar-group">
      <label class="toggle-label">
        <span class="toggle-text">同比对比</span>
        <button
          class="toggle-switch"
          :class="{ on: compare }"
          role="switch"
          :aria-checked="compare"
          @click="emit('update:compare', !compare)"
        ><span class="toggle-thumb"></span></button>
      </label>
    </div>

    <div class="toolbar-group">
      <select class="tb-select" :value="refreshInterval" @change="onRefreshChange">
        <option v-for="opt in refreshOptions" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
      </select>
    </div>

    <div class="toolbar-group">
      <button class="tb-btn tb-btn--ghost" @click="emit('export')">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
          <polyline points="7 10 12 15 17 10" />
          <line x1="12" y1="15" x2="12" y2="3" />
        </svg>
        导出
      </button>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  days: { type: Number, default: 7 },
  compare: { type: Boolean, default: false },
  refreshInterval: { type: Number, default: 0 },
})

const emit = defineEmits(['update:days', 'update:compare', 'update:refreshInterval', 'export'])

const dayOptions = [
  { label: '7 天', value: 7 },
  { label: '30 天', value: 30 },
  { label: '90 天', value: 90 },
]

const refreshOptions = [
  { label: '关闭', value: 0 },
  { label: '30s', value: 30 },
  { label: '60s', value: 60 },
  { label: '120s', value: 120 },
]

function onRefreshChange(e) {
  emit('update:refreshInterval', Number(e.target.value))
}
</script>

<style scoped>
.dash-toolbar {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-4) 0;
}

.toolbar-group {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.tb-btn {
  padding: var(--space-2) var(--space-4);
  font-size: var(--text-sm);
  font-family: var(--font-body);
  color: var(--text-secondary);
  background: transparent;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: color 0.15s, border-color 0.15s, background 0.15s;
}

.tb-btn:hover {
  color: var(--text-primary);
  border-color: var(--border-default);
}

.tb-btn.active {
  color: var(--text-primary);
  background: var(--bg-surface);
  border-color: var(--text-secondary);
}

.tb-btn--ghost {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  border-color: transparent;
}

.tb-btn--ghost:hover {
  border-color: var(--border-subtle);
}

.toggle-label {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  cursor: pointer;
}

.toggle-text {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  user-select: none;
}

.toggle-switch {
  position: relative;
  width: 34px;
  height: 18px;
  border-radius: 9px;
  border: 1px solid var(--border-subtle);
  background: var(--bg-surface);
  cursor: pointer;
  transition: background 0.2s, border-color 0.2s;
  padding: 0;
}

.toggle-switch.on {
  background: var(--color-accent-subtle);
  border-color: var(--color-accent);
}

.toggle-thumb {
  position: absolute;
  top: 2px;
  left: 2px;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: var(--text-muted);
  transition: transform 0.2s, background 0.2s;
}

.toggle-switch.on .toggle-thumb {
  transform: translateX(16px);
  background: var(--color-accent);
}

.tb-select {
  padding: var(--space-2) var(--space-3);
  font-size: var(--text-sm);
  font-family: var(--font-body);
  color: var(--text-primary);
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  cursor: pointer;
  outline: none;
  transition: border-color 0.15s;
}

.tb-select:focus {
  border-color: var(--color-accent);
}

.tb-select option {
  background: var(--bg-surface);
  color: var(--text-primary);
}
</style>
