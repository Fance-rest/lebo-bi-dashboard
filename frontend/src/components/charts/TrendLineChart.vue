<template>
  <ChartPanel :title="'趋势分析'" :loading="!current?.length">
    <div ref="chartContainer" style="height: 380px" />
  </ChartPanel>
</template>

<script setup>
import { ref, shallowRef, onMounted, watch } from 'vue'
import * as echarts from 'echarts'
import ChartPanel from '../layout/ChartPanel.vue'
import { useChartResize } from '../../composables/useChartResize.js'
import { COLORS, tooltipStyle, axisStyle, areaGradient } from '../../composables/useTheme.js'

const props = defineProps({
  current: { type: Array, default: () => [] },
  previous: { type: Array, default: () => [] },
  days: { type: Number, default: 7 }
})

const chartContainer = ref(null)
const chartInstance = shallowRef(null)

const SERIES_CFG = [
  { key: 'dau', name: 'DAU', color: COLORS.cyan, yAxisIndex: 0 },
  { key: 'active_devices', name: '活跃设备', color: COLORS.green, yAxisIndex: 0 },
  { key: 'cast_count', name: '投屏次数', color: COLORS.amber, yAxisIndex: 0 },
  { key: 'revenue', name: '收入', color: COLORS.violet, yAxisIndex: 1 }
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
  const data = props.current || []
  const prev = props.previous || []
  const xData = data.map(d => formatDate(d.date))

  const currentSeries = SERIES_CFG.map(cfg => ({
    name: cfg.name,
    type: 'line',
    smooth: true,
    symbol: 'none',
    yAxisIndex: cfg.yAxisIndex,
    lineStyle: {
      width: 2,
      type: cfg.key === 'revenue' ? 'dashed' : 'solid'
    },
    itemStyle: { color: cfg.color.main },
    areaStyle: {
      color: areaGradient(cfg.color.light)
    },
    data: data.map(d => d[cfg.key]),
    animationDuration: 800,
    animationEasing: 'cubicOut'
  }))

  const prevSeries = prev.length
    ? SERIES_CFG.map(cfg => ({
        name: cfg.name + '(上期)',
        type: 'line',
        smooth: true,
        symbol: 'none',
        yAxisIndex: cfg.yAxisIndex,
        lineStyle: {
          width: 1.5,
          type: 'dashed',
          opacity: 0.3
        },
        itemStyle: {
          color: cfg.color.main,
          opacity: 0.3
        },
        areaStyle: null,
        data: prev.map(d => d[cfg.key]),
        animationDuration: 800,
        animationEasing: 'cubicOut'
      }))
    : []

  const axis = axisStyle()
  const tooltip = tooltipStyle()

  return {
    tooltip: {
      ...tooltip,
      trigger: 'axis'
    },
    legend: {
      top: 4,
      right: 10,
      textStyle: { color: 'rgba(140, 175, 210, 0.65)', fontSize: 11 },
      icon: 'roundRect',
      itemWidth: 12,
      itemHeight: 3,
      data: SERIES_CFG.map(c => c.name)
    },
    grid: {
      top: 40,
      left: 55,
      right: 60,
      bottom: 30
    },
    xAxis: {
      type: 'category',
      data: xData,
      boundaryGap: false,
      ...axis
    },
    yAxis: [
      {
        type: 'value',
        name: '用户/设备/次数',
        nameTextStyle: { color: 'rgba(140,175,210,0.4)', fontSize: 10, padding: [0, 40, 0, 0] },
        ...axis,
        axisLabel: {
          ...axis.axisLabel,
          formatter: formatWan
        }
      },
      {
        type: 'value',
        name: '收入(元)',
        nameTextStyle: { color: 'rgba(140,175,210,0.4)', fontSize: 10, padding: [0, 0, 0, 40] },
        ...axis,
        splitLine: { show: false },
        axisLabel: {
          ...axis.axisLabel,
          formatter: formatWan
        }
      }
    ],
    series: [...currentSeries, ...prevSeries]
  }
}

onMounted(() => {
  if (!chartContainer.value) return
  chartInstance.value = echarts.init(chartContainer.value)
  if (props.current?.length) {
    chartInstance.value.setOption(buildOption())
  }
})

watch(
  () => [props.current, props.previous, props.days],
  () => {
    if (chartInstance.value && props.current?.length) {
      chartInstance.value.setOption(buildOption(), { notMerge: true })
    }
  },
  { deep: true }
)

useChartResize(chartInstance, chartContainer)
</script>
