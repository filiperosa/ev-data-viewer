<template>
  <Pie :data="chartData" :options="chartOptions" />
</template>

<script lang="ts">
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import { Pie } from 'vue-chartjs'

ChartJS.register(ArcElement, Tooltip, Legend)

export default {
  name: 'App',
  components: {
    Pie
  },
  props: {
    labels: {
      type: Array,
      required: true
    },
    data: {
      type: Array,
      required: true
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
      return {
        labels: this.labels,
        datasets: [
          {
            backgroundColor: ['#41B883', '#E46651', '#00D8FF', '#ffbb00'],
            data: this.data
          }
        ]
      }
    }
  }
}
</script>