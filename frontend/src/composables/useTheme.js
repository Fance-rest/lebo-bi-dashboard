import * as echarts from 'echarts'

/**
 * Refined dark theme — warm slate tones, desaturated chart palette.
 * Follows impeccable design principles: no AI-slop cyan/neon.
 */

export const COLORS = {
  blue:   { main: '#6b8de3', light: 'rgba(107, 141, 227, 0.12)' },
  teal:   { main: '#4ecdc4', light: 'rgba(78, 205, 196, 0.12)' },
  amber:  { main: '#e2a651', light: 'rgba(226, 166, 81, 0.10)' },
  rose:   { main: '#e07067', light: 'rgba(224, 112, 103, 0.10)' },
  violet: { main: '#9b8ec4', light: 'rgba(155, 142, 196, 0.12)' },
  slate:  { main: '#7a8599', light: 'rgba(122, 133, 153, 0.12)' },
}

// Backward-compatible aliases for chart components
COLORS.cyan = COLORS.blue
COLORS.green = COLORS.teal
COLORS.red = COLORS.rose
COLORS.gray = COLORS.slate

export const COLOR_LIST = [
  COLORS.blue.main,
  COLORS.teal.main,
  COLORS.amber.main,
  COLORS.violet.main,
  COLORS.rose.main,
  COLORS.slate.main,
]

// Surface & text colors matching CSS variables
const SURFACE = '#1e2433'
const BORDER = '#2d3548'
const TEXT = '#e4e8f0'
const TEXT_DIM = '#8a93a6'
const GRID = '#262d3d'

export function tooltipStyle() {
  return {
    backgroundColor: SURFACE,
    borderColor: BORDER,
    borderWidth: 1,
    textStyle: {
      color: TEXT,
      fontSize: 12,
      fontFamily: '"DM Sans", "PingFang SC", sans-serif',
    },
    axisPointer: {
      lineStyle: {
        color: BORDER,
        type: 'dashed',
      },
    },
  }
}

export function axisStyle() {
  return {
    axisLine: {
      lineStyle: { color: BORDER },
    },
    axisTick: {
      show: false,
    },
    axisLabel: {
      color: TEXT_DIM,
      fontSize: 11,
      fontFamily: '"DM Sans", "PingFang SC", sans-serif',
    },
    splitLine: {
      lineStyle: { color: GRID },
    },
  }
}

export function areaGradient(colorObj) {
  const color = typeof colorObj === 'string' ? colorObj : colorObj.light
  return new echarts.graphic.LinearGradient(0, 0, 0, 1, [
    { offset: 0, color },
    { offset: 1, color: 'transparent' },
  ])
}
