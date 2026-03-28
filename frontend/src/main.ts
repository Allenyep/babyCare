import { createApp } from 'vue'
import { createPinia } from 'pinia'
import router from './router'
import App from './App.vue'

// Naive UI
import naive from 'naive-ui'

// VueUse Motion
import { MotionPlugin } from '@vueuse/motion'

// Tailwind CSS & Global Styles
import './styles/index.css'

// Legacy styles
import './assets/styles/main.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(naive)
app.use(MotionPlugin)

app.mount('#app')
