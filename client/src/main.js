import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

// Import our custom CSS
import './scss/styles.scss'

// Import all of Bootstrap's JS
import * as bootstrap from 'bootstrap'

import Datepicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css'
import Paginate from "vuejs-paginate-next";

const app = createApp(App);

// https://vue3datepicker.com/
app.component('Datepicker', Datepicker);

// https://www.npmjs.com/package/vuejs-paginate-next
app.component('Paginate', Paginate);

app.mount('#app');
