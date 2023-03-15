import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

// Import our custom CSS
import './scss/styles.scss'

// Import all of Bootstrap's JS
import * as bootstrap from 'bootstrap'

import { createPinia } from 'pinia'
import { useEvDataStore } from './stores/EvDataStore'

import Datepicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
import Paginate from "vuejs-paginate-next";

const pinia = createPinia()
const app = createApp(App);

app.use(pinia);

const evDataStore = useEvDataStore()

// https://vue3datepicker.com/
app.component('Datepicker', Datepicker);

// https://www.npmjs.com/package/vuejs-paginate-next
app.component('Paginate', Paginate);

app.mount('#app');
