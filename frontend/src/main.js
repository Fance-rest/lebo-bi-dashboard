import { createApp } from 'vue'
import * as echarts from 'echarts'
import App from './App.vue'

import './styles/variables.css'
import './styles/global.css'
import './styles/transitions.css'

// Register China GeoJSON for ECharts map charts
import chinaGeoJSON from './assets/china.json'
echarts.registerMap('china', chinaGeoJSON)

const app = createApp(App)
app.mount('#app')
