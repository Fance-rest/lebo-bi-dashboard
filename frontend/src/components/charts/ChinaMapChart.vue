<template>
  <ChartPanel :title="'全国分布'" :loading="!data?.length">
    <div ref="chartContainer" style="height: 380px" />
  </ChartPanel>
</template>

<script setup>
import { ref, shallowRef, onMounted, watch, computed } from 'vue'
import * as echarts from 'echarts'
import ChartPanel from '../layout/ChartPanel.vue'
import { useChartResize } from '../../composables/useChartResize.js'
import { tooltipStyle } from '../../composables/useTheme.js'

const props = defineProps({
  data: { type: Array, default: () => [] }
})

const chartContainer = ref(null)
const chartInstance = shallowRef(null)

const dataMap = computed(() => {
  const m = {}
  ;(props.data || []).forEach(d => { m[d.name] = d })
  return m
})

function buildOption() {
  const items = props.data || []
  const maxVal = items.reduce((mx, d) => Math.max(mx, d.active_users || 0), 0)
  const mapData = items.map(d => ({ name: d.name, value: d.active_users || 0 }))
  const tooltip = tooltipStyle()

  return {
    tooltip: {
      ...tooltip,
      trigger: 'item',
      formatter(params) {
        const d = dataMap.value[params.name]
        if (!d) return params.name
        return [
          `<b>${params.name}</b>`,
          `活跃用户: ${(d.active_users || 0).toLocaleString()}`,
          `投屏次数: ${(d.cast_count || 0).toLocaleString()}`,
          `收入: ${(d.revenue || 0).toLocaleString()} 元`
        ].join('<br/>')
      }
    },
    visualMap: {
      type: 'continuous',
      min: 0,
      max: maxVal || 1,
      left: 20,
      bottom: 20,
      text: ['高', '低'],
      textStyle: { color: 'rgba(140, 175, 210, 0.65)', fontSize: 11 },
      inRange: {
        color: ['#0a1628', '#1a5a8a', '#37a0ff']
      },
      calculable: false,
      itemWidth: 12,
      itemHeight: 100
    },
    series: [
      {
        name: '活跃用户',
        type: 'map',
        map: 'china',
        roam: false,
        data: mapData,
        label: {
          show: false
        },
        emphasis: {
          label: {
            show: true,
            color: '#d4e0f0',
            fontSize: 12
          },
          itemStyle: {
            areaColor: '#4db8ff'
          }
        },
        itemStyle: {
          areaColor: '#0e1a32',
          borderColor: 'rgba(55, 160, 255, 0.15)',
          borderWidth: 0.5
        },
        select: {
          disabled: true
        },
        animationDurationUpdate: 800,
        animationEasingUpdate: 'cubicOut'
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
