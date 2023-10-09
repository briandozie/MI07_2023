import { createApp } from "vue"
import App from "./App.vue"
import router from "./router"
import "bootstrap/dist/css/bootstrap.css"
import "bootstrap-icons/font/bootstrap-icons.css"

import axios from "axios"

axios.defaults.withCredentials = true

createApp(App).use(router).mount("#app")
