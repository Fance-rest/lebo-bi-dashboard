<template>
  <ChartPanel :title="'渠道收入分布'" :loading="!data?.length">
    <div ref="chartContainer" style="height: 340px" />
  </ChartPanel>
</template>

<script setup>
import { ref, shallowRef, onMounted, watch } from 'vue'
import * as echarts from 'echarts'
import ChartPanel from '../layout/ChartPanel.vue'
import { useChartResize } from '../../composables/useChartResize.js'
import { COLORS, tooltipStyle, axisStyle } from '../../composables/useTheme.js'

const props = defineProps({
  data: { type: Array, default: () => [] }
})

const chartContainer = ref(null)
const chartInstance = shallowRef(null)

const CHANNELS = [
  { key: 'VIP会员', color: COLORS.cyan.main },
  { key: '广告收入', color: COLORS.green.main },
  { key: '内容分成', color: COLORS.amber.main },
  { key: '增值服务', color: COLORS.violet.main },
  { key: '硬件合作', color: COLORS.gray.main }
]

function formatWan(val) {
  if (val >= 10000) return (val / 10000).toFixed(1) + '万'
  return val
}

function formatDate(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${m}-${day}`
}

function buildOption() {
  const items = props.data || []
  const xData = items.map(d => formatDate(d.date))
  const axis = axisStyle()
  const tooltip = tooltipStyle()

  const series = CHANNELS.map((ch, idx) => ({
    name: ch.key,
    type: 'bar',
    stack: 'revenue',
    data: items.map(d => d[ch.key] || 0),
    itemStyle: {
      color: ch.color,
      borderRadius: idx === CHANNELS.length - 1 ? [2, 2, 0, 0] : [0, 0, 0, 0]
    },
    barMaxWidth: 24,
    animationDuration: 800,
    animationEasing: 'cubicOut'
  }))

  return {
    tooltip: {
      ...tooltip,
      trigger: 'axis',
      axisPointer: {
        type: 'shadow',
        shadowStyle: { color: 'rgba(55, 160, 255, 0.04)' }
      },
      formatter(params) {
        if (!params || !params.length) return ''
        const header = params[0].axisValueLabel
        let total = 0
        const lines = params.map(p => {
          total += p.value || 0
          return `${p.marker} ${p.seriesName}: ${(p.value || 0).toLocaleString()} 元`
        })
        lines.push(`<b>合计: ${total.toLocaleString()} 元</b>`)
        return [header, ...lines].join('<br/>')
      }
    },
    legend: {
      top: 4,
      right: 10,
      textStyle: { color: 'rgba(140, 175, 210, 0.65)', fontSize: 11 },
      icon: 'roundRect',
      itemWidth: 12,
      itemHeight: 8,
      data: CHANNELS.map(c => c.key)
    },
    grid: {
      top: 40,
      left: 55,
      right: 20,
      bottom: 30
    },
    xAxis: {
      type: 'category',
      data: xData,
      ...axis
    },
    yAxis: {
      type: 'value',
      name: '收入(元)',
      nameTextStyle: { color: 'rgba(140,175,210,0.4)', fontSize: 10 },
      ...axis,
      axisLabel: {
        ...axis.axisLabel,
        formatter: formatWan
      }
    },
    series
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
