<template>
  <ChartPanel :title="title" :loading="loading">
    <div class="retention-wrapper">
      <!-- Line Chart -->
      <div ref="containerRef" class="retention-line-chart" />

      <!-- Cohort Table -->
      <div class="retention-table-wrap">
        <table class="retention-table">
          <thead>
            <tr>
              <th>周期</th>
              <th>新增用户</th>
              <th>Day 1</th>
              <th>Day 3</th>
              <th>Day 7</th>
              <th>Day 14</th>
              <th>Day 30</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="row in data" :key="row.cohort_week">
              <td class="cell-label">{{ row.cohort_week }}</td>
              <td class="cell-users">{{ row.initial_users.toLocaleString() }}</td>
              <td :style="cellBg(row.day1)">{{ row.day1 }}%</td>
              <td :style="cellBg(row.day3)">{{ row.day3 }}%</td>
              <td :style="cellBg(row.day7)">{{ row.day7 }}%</td>
              <td :style="cellBg(row.day14)">{{ row.day14 }}%</td>
              <td :style="cellBg(row.day30)">{{ row.day30 }}%</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </ChartPanel>
</template>

<script setup>
import { ref, shallowRef, onMounted, watch, computed } from 'vue'
import * as echarts from 'echarts'
import ChartPanel from '../layout/ChartPanel.vue'
import { useChartResize } from '../../composables/useChartResize.js'
import { COLORS, tooltipStyle, axisStyle, areaGradient } from '../../composables/useTheme.js'

const props = defineProps({
  title: { type: String, default: '' },
  loading: { type: Boolean, default: false },
  data: { type: Array, default: () => [] }
})

const containerRef = ref(null)
const chartInstance = shallowRef(null)

const PERIODS = ['Day 1', 'Day 3', 'Day 7', 'Day 14', 'Day 30']
const PERIOD_KEYS = ['day1', 'day3', 'day7', 'day14', 'day30']

function cellBg(value) {
  const alpha = (value / 100) * 0.5
  return {
    backgroundColor: `rgba(0, 212, 170, ${alpha.toFixed(3)})`
  }
}

function computeAverages(data) {
  if (!data.length) return PERIOD_KEYS.map(() => 0)
  return PERIOD_KEYS.map((key) => {
    const sum = data.reduce((acc, row) => acc + (row[key] || 0), 0)
    return parseFloat((sum / data.length).toFixed(1))
  })
}

function buildOption(data) {
  const averages = computeAverages(data)
  const axis = axisStyle()

  return {
    tooltip: {
      trigger: 'axis',
      ...tooltipStyle(),
      formatter(params) {
        const p = params[0]
        return `${p.name}<br/>
          <span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:${COLORS.green.main};margin-right:6px;"></span>
          平均留存率: <b>${p.value}%</b>`
      }
    },
    grid: {
      top: 30,
      right: 20,
      bottom: 25,
      left: 50
    },
    xAxis: {
      type: 'category',
      data: PERIODS,
      boundaryGap: false,
      ...axis
    },
    yAxis: {
      type: 'value',
      min: 0,
      max: 50,
      axisLabel: {
        ...axis.axisLabel,
        formatter: '{value}%'
      },
      axisLine: axis.axisLine,
      axisTick: axis.axisTick,
      splitLine: axis.splitLine
    },
    series: [
      {
        type: 'line',
        data: averages,
        smooth: true,
        symbol: 'circle',
        symbolSize: 8,
        lineStyle: {
          color: COLORS.green.main,
          width: 2
        },
        itemStyle: {
          color: COLORS.green.main,
          borderColor: '#0c1527',
          borderWidth: 2
        },
        areaStyle: {
          color: areaGradient(COLORS.green.light)
        },
        label: {
          show: true,
          color: 'rgba(200, 220, 240, 0.85)',
          fontSize: 11,
          formatter: '{c}%'
        },
        animationDuration: 800,
        animationEasing: 'cubicOut'
      }
    ]
  }
}

onMounted(() => {
  if (containerRef.value) {
    chartInstance.value = echarts.init(containerRef.value)
    if (props.data.length) {
      chartInstance.value.setOption(buildOption(props.data))
    }
  }
})

watch(
  () => props.data,
  (newData) => {
    if (chartInstance.value && newData.length) {
      chartInstance.value.setOption(buildOption(newData), true)
    }
  },
  { deep: true }
)

useChartResize(chartInstance, containerRef)
</script>

<style scoped>
.retention-wrapper {
  display: flex;
  flex-direction: column;
}

.retention-line-chart {
  width: 100%;
  height: 200px;
}

.retention-table-wrap {
  max-height: 200px;
  overflow-y: auto;
  margin-top: 4px;
}

.retention-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
  color: rgba(200, 220, 240, 0.85);
}

.retention-table th {
  position: sticky;
  top: 0;
  background: rgba(8, 14, 36, 0.95);
  color: rgba(140, 175, 210, 0.6);
  font-weight: 500;
  text-align: center;
  padding: 6px 8px;
  border-bottom: 1px solid rgba(55, 160, 255, 0.1);
  white-space: nowrap;
}

.retention-table td {
  text-align: center;
  padding: 5px 8px;
  border-bottom: 1px solid rgba(55, 160, 255, 0.06);
  white-space: nowrap;
}

.retention-table .cell-label {
  color: rgba(140, 175, 210, 0.7);
  text-align: left;
}

.retention-table .cell-users {
  color: rgba(200, 220, 240, 0.7);
}

.retention-table tbody tr:hover {
  background: rgba(55, 160, 255, 0.04);
}

/* Scrollbar styling for dark theme */
.retention-table-wrap::-webkit-scrollbar {
  width: 4px;
}

.retention-table-wrap::-webkit-scrollbar-track {
  background: transparent;
}

.retention-table-wrap::-webkit-scrollbar-thumb {
  background: rgba(55, 160, 255, 0.15);
  border-radius: 2px;
}
</style>
