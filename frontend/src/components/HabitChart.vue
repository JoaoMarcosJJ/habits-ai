<script setup lang="ts">
import { computed } from 'vue';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js';
import { Bar } from 'vue-chartjs';
import type { HabitLog } from '@/types/habit';

// Registrar componentes do Chart.js
ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend);

const props = defineProps<{
  logs: HabitLog[];
}>();

// Lógica para calcular os últimos 7 dias
const chartData = computed(() => {
  const labels = [];
  const data = [];
  const today = new Date();

  // Loop pelos últimos 7 dias 
  for (let i = 6; i >= 0; i--) {
    const d = new Date();
    d.setDate(today.getDate() - i);
    
    const dayName = d.toLocaleDateString('pt-BR', { weekday: 'short' }).slice(0, 3);
    const dateStr = d.toISOString().split('T')[0];

    // Verifica se existe log para este dia
    const isCompleted = props.logs.some(log => log.completed_date === dateStr);

    labels.push(dayName);
    data.push(isCompleted ? 1 : 0);
  }

  return {
    labels,
    datasets: [{
      label: 'Completado',
      data: data,
      backgroundColor: '#42b983',
      borderRadius: 4,
      barThickness: 20
    }]
  };
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: { enabled: false }
  },
  scales: {
    y: { display: false, min: 0, max: 1 }, 
    x: { grid: { display: false } } 
  }
};
</script>

<template>
  <div class="chart-wrapper">
    <Bar :data="chartData" :options="chartOptions" />
  </div>
</template>

<style scoped>
.chart-wrapper {
  height: 100px;
  width: 100%;
}
</style>