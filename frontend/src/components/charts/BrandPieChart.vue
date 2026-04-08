<template>
  <ChartPanel :title="title" :loading="loading">
    <div ref="containerRef" class="brand-pie-chart" />
  </ChartPanel>
</template>

<script setup>
import { ref, shallowRef, onMounted, watch } from 'vue'
import * as echarts from 'echarts'
import ChartPanel from '../layout/ChartPanel.vue'
import { useChartResize } from '../../composables/useChartResize.js'
import { COLORS, COLOR_LIST, tooltipStyle } from '../../composables/useTheme.js'

const props = defineProps({
  title: { type: String, default: '' },
  loading: { type: Boolean, default: false },
  data: { type: Array, default: () => [] }
})

const containerRef = ref(null)
const chartInstance = shallowRef(null)

function buildOption(data) {
  return {
    tooltip: {
      trigger: 'item',
      ...tooltipStyle(),
      formatter(params) {
        return `<span style="display:inline-block;width:8px;height:8px;border-radius:50%;background:${params.color};margin-right:6px;"></span>${params.name}: <b>${params.value}%</b>`
      }
    },
    color: COLOR_LIST,
    series: [
      {
        type: 'pie',
        radius: ['44%', '72%'],
        center: ['50%', '55%'],
        avoidLabelOverlap: true,
        itemStyle: {
          borderColor: '#080b1a',
          borderWidth: 3,
          borderRadius: 5
        },
        label: {
          show: true,
          color: 'rgba(200, 220, 240, 0.85)',
          fontSize: 12,
          formatter: '{b}\n{d}%'
        },
        labelLine: {
          lineStyle: {
            color: 'rgba(55, 160, 255, 0.3)'
          }
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 14,
            fontWeight: 'bold',
            color: '#e8f0ff'
          },
          itemStyle: {
            shadowBlur: 20,
            shadowColor: 'rgba(55, 160, 255, 0.4)',
            shadowOffsetX: 0,
            shadowOffsetY: 0
          }
        },
        animationType: 'scale',
        animationDuration: 800,
        animationEasing: 'cubicOut',
        data: data
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
.brand-pie-chart {
  width: 100%;
  height: 340px;
}
</style>
