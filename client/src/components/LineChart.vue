<template>
    <Line :data="chartData" :options="chartOptions" />
</template>

<script lang="ts">
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    TimeScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
} from 'chart.js'
import { Line } from 'vue-chartjs'

ChartJS.register(
    CategoryScale,
    LinearScale,
    TimeScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
)
import 'chartjs-adapter-date-fns';

export default {
    name: 'LineChart',
    components: {
        Line
    },
    props: {
        // labels: {
        //     type: Array,
        //     required: true
        // },
        // data: {
        //     type: Array,
        //     required: true
        // },
        // caption: {
        //     type: String,
        //     required: false
        // },
        // color: {
        //     type: String,
        //     required: false
        // }
        datasets: {
            type: Array,
            required: true
        }
    },
    data() {
        return {
            chartOptions: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    xAxis: {
                        type: 'time',
                        time: {
                            unit: 'minute', 
                            displayFormats: {
                                millisecond: ''
                            }
                        }
                    } 
                }
            }
        }
    },
    computed: {
        chartData() {
            return{
                datasets: this.datasets
            }
        }
    }
}
</script>
