import '../node_modules/onyks-web-ui-system/dist/general.css'
import 'onyks-web-ui-system'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)
app.use(router)
app.mount('#app')