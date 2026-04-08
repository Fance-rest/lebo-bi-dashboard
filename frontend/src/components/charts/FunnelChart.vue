<template>
  <ChartPanel :title="title" :loading="loading">
    <div ref="containerRef" class="funnel-chart" />
  </ChartPanel>
</template>

<script setup>
import { ref, shallowRef, onMounted, watch } from 'vue'
import * as echarts from 'echarts'
import ChartPanel from '../layout/ChartPanel.vue'
import { useChartResize } from '../../composables/useChartResize.js'
import { COLORS, tooltipStyle } from '../../composables/useTheme.js'

const STAGE_COLORS = [
  COLORS.cyan.main,
  COLORS.green.main,
  COLORS.amber.main,
  COLORS.violet.main,
  COLORS.red.main
]

const props = defineProps({
  title: { type: String, default: '' },
  loading: { type: Boolean, default: false },
  data: { type: Array, default: () => [] }
})

const containerRef = ref(null)
const chartInstance = shallowRef(null)

function buildOption(data) {
  const seriesData = data.map((item, index) => ({
    name: item.name,
    value: item.value,
    rate: item.rate,
    itemStyle: {
      color: STAGE_COLORS[index % STAGE_COLORS.length],
      borderColor: '#080b1a',
      borderWidth: 2
    }
  }))

  return {
    tooltip: {
      trigger: 'item',
      ...tooltipStyle(),
      formatter(params) {
        const d = params.data
        return `<span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:${params.color};margin-right:6px;"></span>${d.name}<br/>
          <span style="margin-left:14px;">数量: <b>${d.value.toLocaleString()}</b></span><br/>
          <span style="margin-left:14px;">转化率: <b>${d.rate}%</b></span>`
      }
    },
    series: [
      {
        type: 'funnel',
        top: 60,
        bottom: 20,
        left: '15%',
        width: '70%',
        sort: 'descending',
        gap: 4,
        label: {
          show: true,
          position: 'inside',
          color: 'rgba(240, 248, 255, 0.95)',
          fontSize: 13,
          fontWeight: 500,
          formatter(params) {
            return `${params.data.name}\n${params.data.rate}%`
          }
        },
        labelLine: {
          show: false
        },
        emphasis: {
          itemStyle: {
            opacity: 1,
            shadowBlur: 12,
            shadowColor: 'rgba(55, 160, 255, 0.3)'
          }
        },
        animationDuration: 800,
        animationEasing: 'cubicOut',
        data: seriesData
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
.funnel-chart {
  width: 100%;
  height: 340px;
}
</style>
