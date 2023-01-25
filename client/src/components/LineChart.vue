<template>
    <Line :data="chartData" :options="chartOptions" />
</template>

<script lang="ts">
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
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
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
)

export default {
    name: 'LineChart',
    components: {
        Line
    },
    props: {
        labels: {
            type: Array,
            required: true
        },
        data: {
            type: Array,
            required: true
        },
        caption: {
            type: String,
            required: false
        },
        color: {
            type: String,
            required: false
        }
    },
    data() {
        return {
            chartOptions: {
                responsive: true,
                maintainAspectRatio: false
            }
        }
    },
    computed: {
        chartData() {
            return{
                labels: this.labels,
                datasets: [
                    {
                    label: this.caption ? this.caption : '',
                    backgroundColor: this.color ? this.color : '#f87979',
                    data: this.data
                    }
                ]
            }
        }
    }
}
</script>
