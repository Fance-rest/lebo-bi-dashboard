<template>
  <ChartPanel :title="title" :loading="loading">
    <div ref="containerRef" class="gauge-chart" />
  </ChartPanel>
</template>

<script setup>
import { ref, shallowRef, onMounted, watch } from 'vue'
import * as echarts from 'echarts'
import ChartPanel from '../layout/ChartPanel.vue'
import { useChartResize } from '../../composables/useChartResize.js'
import { COLORS, tooltipStyle } from '../../composables/useTheme.js'

const props = defineProps({
  title: { type: String, default: '' },
  loading: { type: Boolean, default: false },
  items: { type: Array, default: () => [] }
})

const containerRef = ref(null)
const chartInstance = shallowRef(null)

function getCenter(index, total) {
  if (total === 1) return ['50%', '55%']
  if (total === 2) return [index === 0 ? '30%' : '70%', '55%']
  // 3 items
  const positions = ['25%', '50%', '75%']
  return [positions[index], '55%']
}

function buildOption(items) {
  const series = items.map((item, index) => {
    const colorObj = COLORS[item.color] || COLORS.cyan
    const pct = Math.min((item.value / item.target) * 100, 100)
    const pctRatio = pct / 100

    return {
      type: 'gauge',
      center: getCenter(index, items.length),
      radius: '70%',
      startAngle: 225,
      endAngle: -45,
      min: 0,
      max: 100,
      splitNumber: 10,
      pointer: {
        show: false
      },
      progress: {
        show: false
      },
      axisLine: {
        lineWidth: 18,
        lineStyle: {
          width: 18,
          color: [
            [pctRatio, colorObj.main],
            [1, 'rgba(55, 160, 255, 0.08)']
          ]
        }
      },
      axisTick: { show: false },
      splitLine: { show: false },
      axisLabel: { show: false },
      title: {
        show: true,
        offsetCenter: [0, '75%'],
        color: 'rgba(140, 175, 210, 0.6)',
        fontSize: 13
      },
      detail: {
        offsetCenter: [0, '10%'],
        valueAnimation: true,
        formatter: `${pct.toFixed(1)}%`,
        color: colorObj.main,
        fontSize: 22,
        fontWeight: 'bold'
      },
      data: [
        {
          value: pct,
          name: item.label
        }
      ]
    }
  })

  return {
    tooltip: {
      ...tooltipStyle(),
      formatter(params) {
        const item = items.find((i) => i.label === params.name)
        if (!item) return params.name
        const pct = ((item.value / item.target) * 100).toFixed(1)
        return `${params.name}<br/>
          <span style="color:${COLORS[item.color]?.main || '#37a0ff'}">
            ${item.value.toLocaleString()} / ${item.target.toLocaleString()}
          </span>
          <br/>${pct}%`
      }
    },
    series
  }
}

onMounted(() => {
  if (containerRef.value) {
    chartInstance.value = echarts.init(containerRef.value)
    if (props.items.length) {
      chartInstance.value.setOption(buildOption(props.items))
    }
  }
})

watch(
  () => props.items,
  (newItems) => {
    if (chartInstance.value && newItems.length) {
      chartInstance.value.setOption(buildOption(newItems), true)
    }
  },
  { deep: true }
)

useChartResize(chartInstance, containerRef)
</script>

<style scoped>
.gauge-chart {
  width: 100%;
  height: 340px;
}
</style>
