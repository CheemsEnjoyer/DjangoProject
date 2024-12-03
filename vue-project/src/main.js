import { createApp } from 'vue'
import { createPinia } from 'pinia'
import "bootstrap/dist/css/bootstrap.css"
import "bootstrap/dist/js/bootstrap"
import "bootstrap-icons/font/bootstrap-icons.min.css"
import App from './App.vue'
import router from './router';
import useUserProfileStore from './stores/userProfileStore';
const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
