<template>
  <div class="dashboard">
    <DashHeader :ws-status="wsStatus" :countdown="countdown" />
    <DashToolbar
      :days="days"
      :compare="compare"
      :refresh-interval="refreshInterval"
      @update:days="onDaysChange"
      @update:compare="onCompareChange"
      @update:refresh-interval="onRefreshChange"
      @export="handleExport"
    />

    <MetricCardRow :summary="summary" />

    <!-- Row 1: Trend + Map -->
    <div class="chart-row row-2col">
      <TrendLineChart
        :current="dailyCurrent"
        :previous="compare ? dailyPrevious : null"
        :days="days"
        :loading="loadingMetrics"
      />
      <ChinaMapChart :data="regionalData" :loading="loadingRegional" />
    </div>

    <!-- Row 2: Channel + Heatmap + Pie -->
    <div class="chart-row row-3col">
      <ChannelBarChart :data="channelData" :loading="loadingChannels" />
      <HourlyHeatmap :data="hourlyData" :loading="loadingHourly" />
      <BrandPieChart title="设备品牌分布" :data="brandsData" :loading="loadingBrands" />
    </div>

    <!-- Row 3: Funnel + Gauge + Retention -->
    <div class="chart-row row-3col">
      <FunnelChart title="转化漏斗" :data="funnelData" :loading="loadingFunnel" />
      <GaugeChart title="KPI 达成率" :items="gaugeItems" :loading="loadingMetrics" />
      <RetentionChart title="用户留存分析" :data="retentionData" :loading="loadingRetention" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'

// Layout
import DashHeader from '../components/layout/DashHeader.vue'
import DashToolbar from '../components/layout/DashToolbar.vue'

// Cards
import MetricCardRow from '../components/cards/MetricCardRow.vue'

// Charts
import TrendLineChart from '../components/charts/TrendLineChart.vue'
import ChinaMapChart from '../components/charts/ChinaMapChart.vue'
import ChannelBarChart from '../components/charts/ChannelBarChart.vue'
import HourlyHeatmap from '../components/charts/HourlyHeatmap.vue'
import BrandPieChart from '../components/charts/BrandPieChart.vue'
import GaugeChart from '../components/charts/GaugeChart.vue'
import FunnelChart from '../components/charts/FunnelChart.vue'
import RetentionChart from '../components/charts/RetentionChart.vue'

// API
import { fetchMetrics, fetchHourlyMetrics } from '../api/metrics.js'
import { fetchBrands } from '../api/brands.js'
import { fetchRegionalData } from '../api/regional.js'
import { fetchRetention } from '../api/retention.js'
import { fetchFunnel } from '../api/funnel.js'
import { fetchChannels } from '../api/channels.js'
import { downloadCSV } from '../api/exportData.js'

// Composables
import { useAutoRefresh } from '../composables/useAutoRefresh.js'
import { useWebSocket } from '../composables/useWebSocket.js'

// --- State ---
const days = ref(7)
const compare = ref(false)
const refreshInterval = ref(0)

// Data
const dailyCurrent = ref([])
const dailyPrevious = ref([])
const summary = ref({})
const hourlyData = ref([])
const brandsData = ref([])
const regionalData = ref([])
const retentionData = ref([])
const funnelData = ref([])
const channelData = ref([])

// Loading states
const loadingMetrics = ref(false)
const loadingHourly = ref(false)
const loadingBrands = ref(false)
const loadingRegional = ref(false)
const loadingRetention = ref(false)
const loadingFunnel = ref(false)
const loadingChannels = ref(false)

// Gauge items derived from summary
const gaugeItems = computed(() => [
  { label: 'DAU 达成率', value: summary.value.dau || 0, target: 150000, color: 'cyan' },
  { label: '月收入达成率', value: summary.value.revenue || 0, target: days.value === 7 ? 120000 : days.value === 30 ? 500000 : 1500000, color: 'violet' },
])

// --- WebSocket ---
const { data: wsData, status: wsStatus, connect: wsConnect, disconnect: wsDisconnect } = useWebSocket()

// --- Auto Refresh ---
const { countdown, start: startRefresh, stop: stopRefresh } = useAutoRefresh(fetchAllData, refreshInterval)

// --- Data Fetching ---
async function fetchAllData() {
  const promises = []

  loadingMetrics.value = true
  promises.push(
    fetchMetrics(days.value, compare.value).then(res => {
      summary.value = res.summary || {}
      dailyCurrent.value = res.daily || res.current || []
      if (res.previous) dailyPrevious.value = res.previous
      else dailyPrevious.value = []
    }).finally(() => { loadingMetrics.value = false })
  )

  loadingHourly.value = true
  promises.push(
    fetchHourlyMetrics(Math.min(days.value, 7)).then(res => {
      hourlyData.value = res.hourly || []
    }).finally(() => { loadingHourly.value = false })
  )

  loadingBrands.value = true
  promises.push(
    fetchBrands().then(res => {
      brandsData.value = res.brands || []
    }).finally(() => { loadingBrands.value = false })
  )

  loadingRegional.value = true
  promises.push(
    fetchRegionalData().then(res => {
      regionalData.value = res.provinces || []
    }).finally(() => { loadingRegional.value = false })
  )

  loadingRetention.value = true
  promises.push(
    fetchRetention().then(res => {
      retentionData.value = res.cohorts || []
    }).finally(() => { loadingRetention.value = false })
  )

  loadingFunnel.value = true
  promises.push(
    fetchFunnel().then(res => {
      funnelData.value = (res.stages || []).map(s => ({
        name: s.label || s.name,
        value: s.count || s.value,
        rate: s.rate_from_start != null ? s.rate_from_start : s.rate
      }))
    }).finally(() => { loadingFunnel.value = false })
  )

  loadingChannels.value = true
  promises.push(
    fetchChannels(days.value).then(res => {
      channelData.value = res.channels || res.daily || []
    }).finally(() => { loadingChannels.value = false })
  )

  await Promise.allSettled(promises)
}

// --- Event Handlers ---
function onDaysChange(val) {
  days.value = val
}

function onCompareChange(val) {
  compare.value = val
}

function onRefreshChange(val) {
  refreshInterval.value = val
  if (val > 0) startRefresh(val)
  else stopRefresh()
}

function handleExport() {
  downloadCSV('metrics', days.value)
}

// --- Watchers ---
watch([days, compare], () => {
  fetchAllData()
})

// --- Lifecycle ---
onMounted(() => {
  fetchAllData()
  wsConnect()
})

onUnmounted(() => {
  wsDisconnect()
  stopRefresh()
})
</script>

<style scoped>
.dashboard {
  max-width: 1600px;
  margin: 0 auto;
  padding: 0 24px 40px;
}

.chart-row {
  display: grid;
  gap: 16px;
  margin-top: 16px;
}

.row-2col {
  grid-template-columns: 3fr 2fr;
}

.row-3col {
  grid-template-columns: 1fr 1fr 1fr;
}

@media (max-width: 1200px) {
  .row-2col { grid-template-columns: 1fr; }
  .row-3col { grid-template-columns: 1fr 1fr; }
}

@media (max-width: 768px) {
  .row-3col { grid-template-columns: 1fr; }
  .dashboard { padding: 0 12px 24px; }
}
</style>
