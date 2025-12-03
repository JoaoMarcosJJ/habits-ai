<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { useHabitStore } from '@/stores/habitStore';
import { Trash2, BarChart2 } from 'lucide-vue-next';
import HabitChart from '@/components/HabitChart.vue';
import ChatWidget from '@/components/ChatWidget.vue';

const habitStore = useHabitStore();
const newHabitName = ref('');
const expandedHabitId = ref<number | null>(null);

onMounted(() => {
  habitStore.fetchHabits();
});

const handleAddHabit = async () => {
  if (!newHabitName.value.trim()) return;
  await habitStore.addHabit({ name: newHabitName.value });
  newHabitName.value = '';
};

const handleAISuggest = async () => {
  if (!newHabitName.value.trim()) {
    alert('Por favor, escreva uma meta (ex: "Correr maratona") para a IA gerar hábitos.');
    return;
  }
  await habitStore.generateHabitsFromGoal(newHabitName.value);
  newHabitName.value = '';
};

const handleDelete = async (habitId: number) => {
  await habitStore.removeHabit(habitId);
};

const isCompletedToday = (habit: any) => {
  const today = new Date().toISOString().split('T')[0];
  return habit.logs.some((log: any) => log.completed_date === today);
};

const handleToggle = async (habit: any) => {
  await habitStore.toggleHabitCompletion(habit.id);
};

const toggleChart = (id: number) => {
  if (expandedHabitId.value === id) {
    expandedHabitId.value = null;
  } else {
    expandedHabitId.value = id;
  }
};
</script>

<template>
  <div class="app-wrapper">
    <header class="app-header">
      <div class="logo-container">
        <h1>🌱 Habits <span class="highlight">GenAI</span></h1>
        <p class="subtitle">Transforme metas em conquistas diárias.</p>
      </div>
    </header>

    <main class="main-container">
      <div class="control-bar">
        <input 
          v-model="newHabitName" 
          @keyup.enter="handleAddHabit"
          type="text" 
          placeholder="✨ Digite um novo hábito ou meta..." 
          :disabled="habitStore.isLoading || habitStore.isGenerating"
        />
        
        <div class="actions">
          <button @click="handleAddHabit" class="btn btn-primary" :disabled="habitStore.isLoading">
            Adicionar
          </button>

          <button 
            @click="handleAISuggest" 
            class="btn btn-ai"
            :disabled="habitStore.isLoading || habitStore.isGenerating"
            title="Gerar hábitos com IA"
          >
            {{ habitStore.isGenerating ? 'Criando...' : '✨ IA' }}
          </button>
        </div>
      </div>

      <div v-if="habitStore.error" class="error-banner">
        ⚠️ {{ habitStore.error }}
      </div>

      <div class="habit-list">
        <div v-if="habitStore.habits.length === 0 && !habitStore.isLoading" class="empty-state">
          <div class="empty-icon">📝</div>
          <h3>Sua lista está vazia</h3>
          <p>Adicione um hábito manualmente ou peça ajuda à IA!</p>
        </div>

        <div 
          v-for="habit in habitStore.habits" 
          :key="habit.id" 
          class="habit-card-wrapper"
        >
          <div 
            class="habit-card"
            :class="{ 'card-completed': isCompletedToday(habit) }"
          >
            <div class="card-left">
              <label class="custom-checkbox">
                <input 
                  type="checkbox" 
                  :checked="isCompletedToday(habit)"
                  @change="handleToggle(habit)"
                />
                <span class="checkmark"></span>
              </label>
              
              <div class="habit-details">
                <span class="habit-name">{{ habit.name }}</span>
                <div class="habit-meta">
                  <span class="streak-badge" :class="{ 'has-streak': habit.logs.length > 0 }">
                    🔥 {{ habit.logs.length }} dias
                  </span>
                </div>
              </div>
            </div>

            <div class="card-actions">
              <button 
                class="icon-btn" 
                @click="toggleChart(habit.id)"
                :class="{ 'active': expandedHabitId === habit.id }"
                title="Ver estatísticas"
              >
                <BarChart2 size="20" />
              </button>
              
              <button 
                class="icon-btn delete-btn" 
                @click="handleDelete(habit.id)"
                title="Excluir hábito"
              >
                <Trash2 size="20" />
              </button>
            </div>
          </div>

          <transition name="expand">
            <div v-if="expandedHabitId === habit.id" class="chart-container">
              <div class="chart-header">
                <span>Desempenho Semanal</span>
              </div>
              <HabitChart :logs="habit.logs" />
            </div>
          </transition>
        </div>
      </div>
    </main>

    <ChatWidget />
  </div>
</template>

<style scoped>
/* Layout Global */
.app-wrapper {
  min-height: 100vh;
  font-family: 'Inter', system-ui, -apple-system, sans-serif;
  color: #e0e0e0;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding-bottom: 80px;}

.main-container {
  width: 100%;
  max-width: 800px; 
  padding: 0 20px;
  box-sizing: border-box;
}

/* Cabeçalho */
.app-header {
  margin-top: 40px;
  margin-bottom: 40px;
  text-align: center;
}

.app-header h1 {
  font-size: 3rem;
  font-weight: 800;
  color: #ffffff;
  margin: 0;
  letter-spacing: -1px;
}

.highlight {
  color: #42b983; 
  background: linear-gradient(120deg, #42b983, #2ecc71);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.subtitle {
  color: #888;
  font-size: 1.1rem;
  margin-top: 8px;
}

/* Barra de Controle */
.control-bar {
  display: flex;
  background: #2c2c2c;
  padding: 8px;
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.2);
  margin-bottom: 32px;
  gap: 8px;
  border: 1px solid #3a3a3a;
}

.control-bar input {
  flex: 1;
  background: transparent;
  border: none;
  padding: 12px 16px;
  color: white;
  font-size: 1rem;
  outline: none;
}

.control-bar input::placeholder {
  color: #666;
}

.actions {
  display: flex;
  gap: 8px;
}

.btn {
  padding: 0 20px;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.95rem;
}

.btn-primary {
  background-color: #3a3a3a;
  color: #fff;
}

.btn-primary:hover {
  background-color: #4a4a4a;
}

.btn-ai {
  background: linear-gradient(135deg, #9b59b6, #8e44ad);
  color: white;
  box-shadow: 0 4px 12px rgba(142, 68, 173, 0.3);
}

.btn-ai:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 16px rgba(142, 68, 173, 0.4);
}

/* Lista de Hábitos */
.habit-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.habit-card-wrapper {
  background: #ffffff;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0,0,0,0.05);
  transition: transform 0.2s, box-shadow 0.2s;
}

.habit-card-wrapper:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}

.habit-card {
  padding: 16px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: white;
  color: #1f2937;
  border-left: 6px solid transparent;
}

.card-completed {
  background-color: #f0fdf4;
  border-left-color: #42b983;
}

.card-left {
  display: flex;
  align-items: center;
  gap: 16px;
}

.habit-details {
  display: flex;
  flex-direction: column;
}

.habit-name {
  font-size: 1.1rem;
  font-weight: 600;
  line-height: 1.4;
}

.card-completed .habit-name {
  color: #9ca3af;
  text-decoration: line-through;
}

.habit-meta {
  margin-top: 4px;
}

.streak-badge {
  font-size: 0.8rem;
  color: #9ca3af;
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  gap: 4px;
}

.has-streak {
  color: #e67e22;
}

/* Checkbox */
.custom-checkbox {
  position: relative;
  width: 24px;
  height: 24px;
  cursor: pointer;
  flex-shrink: 0;
}

.custom-checkbox input { opacity: 0; position: absolute; width: 0; height: 0; }

.checkmark {
  position: absolute; top: 0; left: 0; height: 24px; width: 24px;
  background-color: #f3f4f6; border-radius: 50%;
  border: 2px solid #d1d5db; transition: all 0.2s;
}

.custom-checkbox input:checked ~ .checkmark {
  background-color: #42b983; border-color: #42b983;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='white' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='20 6 9 17 4 12'%3E%3C/polyline%3E%3C/svg%3E");
  background-size: 14px; background-position: center; background-repeat: no-repeat;
}

/* Botões de Ação */
.card-actions {
  display: flex;
  gap: 8px;
}

.icon-btn {
  background: transparent;
  border: none;
  padding: 8px;
  border-radius: 8px;
  color: #9ca3af;
  cursor: pointer;
  display: flex;
  transition: all 0.2s;
}

.icon-btn:hover {
  background-color: #f3f4f6;
  color: #4b5563;
}

.icon-btn.active {
  background-color: #e0f2fe;
  color: #0284c7;
}

.delete-btn:hover {
  background-color: #fee2e2;
  color: #ef4444;
}

/* Gráfico e Animações */
.chart-container {
  background-color: #f9fafb;
  border-top: 1px solid #f3f4f6;
  padding: 16px 20px;
}

.chart-header {
  font-size: 0.75rem;
  text-transform: uppercase;
  color: #9ca3af;
  font-weight: 700;
  margin-bottom: 10px;
  letter-spacing: 0.5px;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: #666;
  background: #2a2a2a;
  border-radius: 16px;
  border: 2px dashed #444;
}

.empty-icon { font-size: 3rem; margin-bottom: 10px; }

.error-banner {
  background-color: #ef4444;
  color: white;
  padding: 12px;
  border-radius: 8px;
  text-align: center;
  margin-bottom: 20px;
  font-weight: 500;
}

/* Animação Expandir */
.expand-enter-active,
.expand-leave-active {
  transition: all 0.3s ease-out;
  max-height: 200px;
  opacity: 1;
}

.expand-enter-from,
.expand-leave-to {
  max-height: 0;
  opacity: 0;
  overflow: hidden;
}
</style>