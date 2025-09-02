<template>
  <div>
    <div v-if="isLoading" class="text-center">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Caricamento...</span>
      </div>
    </div>

    <div v-if="error" class="alert alert-danger">
        Si è verificato un errore nel caricamento dei dati. Si prega di riprovare più tardi.
    </div>

    <div v-if="!isLoading && apiData">
      <div v-if="apiData.is_simulated" class="alert alert-warning" role="alert">
        <h4 class="alert-heading">Attenzione!</h4>
        <p>I dati visualizzati in questa dashboard sono <strong>simulati a scopo dimostrativo</strong>. La logica di calcolo non è ancora stata implementata.</p>
      </div>

      <div class="row">
        <div class="col-lg-8">
          <div class="card shadow mb-4">
            <div class="card-header py-3">
              <h6 class="m-0 font-weight-bold text-primary">Riepilogo Redditi Lordi Annui</h6>
            </div>
            <div class="card-body">
              <canvas ref="barChartCanvas"></canvas>
            </div>
          </div>
        </div>
        <div class="col-lg-4">
          <div class="card shadow mb-4">
            <div class="card-header py-3">
              <h6 class="m-0 font-weight-bold text-primary">Recupero Imposte Anno Corrente</h6>
            </div>
            <div class="card-body text-center">
              <canvas ref="gaugeChartCanvas" style="max-width: 250px; margin: auto;"></canvas>
              <div class="mt-2 small">
                Recuperati <strong>{{ formatCurrency(apiData.gauge_chart_data.recupero_attuale) }}</strong> 
                su <strong>{{ formatCurrency(apiData.gauge_chart_data.potenziale_recupero) }}</strong> potenziali.
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="card shadow mb-4">
        <div class="card-header py-3">
          <h6 class="m-0 font-weight-bold text-primary">Consigli per te</h6>
        </div>
        <div class="card-body">
          <ul class="list-group list-group-flush">
            <li v-for="(advice, index) in apiData.advice_data" :key="index" class="list-group-item">{{ advice }}</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

// Custom plugin to draw text in the center of the doughnut chart
const gaugeTextPlugin = {
  id: 'gaugeText',
  afterDraw: (chart) => {
    const { ctx, chartArea: { width, height } } = chart;
    const meta = chart.getDatasetMeta(0);
    const text = chart.options.plugins.gaugeText.text;
    const color = meta.data[0].options.backgroundColor;

    ctx.save();
    // Set font, color, and alignment
    ctx.font = `bold ${height / 5}px sans-serif`;
    ctx.fillStyle = color;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    // Draw the text in the center of the chart area
    ctx.fillText(text, width / 2, height / 2);
    ctx.restore();
  }
};

export default {
  name: 'RiepilogoDashboard',
  data() {
    return {
      isLoading: true,
      error: false,
      apiData: null,
      barChart: null,
      gaugeChart: null,
    };
  },
  watch: {
    apiData(newData) {
      if (newData) {
        this.$nextTick(() => {
          this.renderBarChart();
          this.renderGaugeChart();
        });
      }
    }
  },
  async mounted() {
    this.isLoading = true;
    this.error = false;
    try {
      const response = await axios.get('/api/riepilogo/data/');
      this.apiData = response.data;
    } catch (error) {
      console.error("Error loading summary data:", error);
      this.error = true;
    } finally {
      this.isLoading = false;
    }
  },
  methods: {
    formatCurrency(value) {
        return new Intl.NumberFormat('it-IT', { style: 'currency', currency: 'EUR' }).format(value);
    },
    renderBarChart() {
      if (!this.$refs.barChartCanvas) return;
      const ctx = this.$refs.barChartCanvas.getContext('2d');
      if (this.barChart) this.barChart.destroy();
      
      this.barChart = new Chart(ctx, {
        type: 'bar',
        data: this.apiData.bar_chart_data,
        options: {
          responsive: true,
          // IMPROVEMENT: Set the width of the bars (e.g., 70% of available space)
          barPercentage: 0.7,
          // and the space for the category
          categoryPercentage: 0.8,
          scales: {
            x: { stacked: true },
            y: { stacked: true, ticks: { callback: value => this.formatCurrency(value) } }
          }
        }
      });
    },
    renderGaugeChart() {
      if (!this.$refs.gaugeChartCanvas) return;
      const ctx = this.$refs.gaugeChartCanvas.getContext('2d');
      const data = this.apiData.gauge_chart_data;
      const percentage = (data.recupero_attuale / data.potenziale_recupero) * 100;
      
      let gaugeColor;
      if (percentage < 33) {
        gaugeColor = '#e74a3b'; // Red
      } else if (percentage < 66) {
        gaugeColor = '#f6c23e'; // Orange
      } else {
        gaugeColor = '#1cc88a'; // Green
      }

      if (this.gaugeChart) this.gaugeChart.destroy();
      
      this.gaugeChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
          labels: ['Recuperato', 'Potenziale Residuo'],
          datasets: [{
            data: [data.recupero_attuale, Math.max(0, data.potenziale_recupero - data.recupero_attuale)],
            backgroundColor: [gaugeColor, '#e9ecef'],
            borderColor: ['#fff', '#fff'],
          }]
        },
        options: {
          responsive: true,
          cutout: '70%',
          plugins: {
            legend: { display: false },
            tooltip: { enabled: false },
            gaugeText: {
              text: `${percentage.toFixed(1)}%`
            }
          }
        },
        plugins: [gaugeTextPlugin]
      });
    }
  }
};
</script>

<style scoped>
.card-header {
    background-color: #f8f9fc;
}
.font-weight-bold {
    font-weight: 700 !important;
}
.text-primary {
    color: #4e73df !important;
}
</style>
