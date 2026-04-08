<template>
  <ChartPanel :title="'活跃时段分布'" :loading="!data?.length">
    <div ref="chartContainer" style="height: 340px" />
  </ChartPanel>
</template>

<script setup>
import { ref, shallowRef, onMounted, watch } from 'vue'
import * as echarts from 'echarts'
import ChartPanel from '../layout/ChartPanel.vue'
import { useChartResize } from '../../composables/useChartResize.js'
import { tooltipStyle, axisStyle } from '../../composables/useTheme.js'

const props = defineProps({
  data: { type: Array, default: () => [] }
})

const chartContainer = ref(null)
const chartInstance = shallowRef(null)

const DAY_LABELS = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
const HOUR_LABELS = Array.from({ length: 24 }, (_, i) => `${i}时`)

function buildOption() {
  const items = props.data || []
  const maxVal = items.reduce((mx, d) => Math.max(mx, d.active_users || 0), 0)

  // ECharts heatmap data format: [xIndex, yIndex, value]
  const heatmapData = items.map(d => [d.hour, d.day, d.active_users || 0])

  const axis = axisStyle()
  const tooltip = tooltipStyle()

  return {
    tooltip: {
      ...tooltip,
      formatter(params) {
        const [hour, day, val] = params.data
        return `${DAY_LABELS[day]} ${hour}时: ${(val || 0).toLocaleString()} 活跃用户`
      }
    },
    grid: {
      top: 20,
      left: 60,
      right: 20,
      bottom: 70
    },
    xAxis: {
      type: 'category',
      data: HOUR_LABELS,
      ...axis,
      splitArea: { show: false }
    },
    yAxis: {
      type: 'category',
      data: DAY_LABELS,
      ...axis,
      splitArea: { show: false }
    },
    visualMap: {
      type: 'continuous',
      min: 0,
      max: maxVal || 1,
      calculable: false,
      orient: 'horizontal',
      left: 'center',
      bottom: 6,
      itemWidth: 12,
      itemHeight: 140,
      text: ['高', '低'],
      textStyle: { color: 'rgba(140, 175, 210, 0.65)', fontSize: 11 },
      inRange: {
        color: ['#0a1628', '#1a5a8a', '#37a0ff']
      }
    },
    series: [
      {
        name: '活跃用户',
        type: 'heatmap',
        data: heatmapData,
        label: {
          show: false
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 6,
            shadowColor: 'rgba(55, 160, 255, 0.4)'
          }
        },
        itemStyle: {
          borderColor: '#080b1a',
          borderWidth: 2
        },
        animationDuration: 800,
        animationEasing: 'cubicOut'
      }
    ]
  }
}

onMounted(() => {
  if (!chartContainer.value) return
  chartInstance.value = echarts.init(chartContainer.value)
  if (props.data?.length) {
    chartInstance.value.setOption(buildOption())
  }
})

watch(
  () => props.data,
  () => {
    if (chartInstance.value && props.data?.length) {
      chartInstance.value.setOption(buildOption(), { notMerge: true })
    }
  },
  { deep: true }
)

useChartResize(chartInstance, chartContainer)
</script>
