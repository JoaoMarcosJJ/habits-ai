import { defineStore } from 'pinia';
import { ref } from 'vue';
import type { Habit, CreateHabitDTO } from '@/types/habit';
import habitService from '@/api/habitService';

export const useHabitStore = defineStore('habit', () => {
    // Estados
    const habits = ref<Habit[]>([]);
    const isLoading = ref(false);
    const error = ref<string | null>(null);
    const isGenerating = ref(false);

    // Ações
    async function fetchHabits() {
        isLoading.value = true;
        error.value = null;
        try {
            habits.value = await habitService.getHabits();
        } catch (err) {
            console.error(err);
            error.value = 'Erro ao carregar hábitos.';
        } finally {
            isLoading.value = false;
        }
    }

    async function addHabit(habitData: CreateHabitDTO) {
        isLoading.value = true;
        try {
            const newHabit = await habitService.createHabit(habitData);
            // Adiciona à lista local imediatamente (UI otimista)
            habits.value.push(newHabit);
        } catch (err) {
            console.error(err);
            error.value = 'Erro ao criar hábito.';
        } finally {
            isLoading.value = false;
        }
    }

    async function generateHabitsFromGoal(goal: string) {
        isGenerating.value = true;
        error.value = null;
        try {
            const suggestions = await habitService.suggestHabits(goal);
            
            // Adiciona cada sugestão como um novo hábito automaticamente
            for (const habitName of suggestions) {
                await addHabit({ name: habitName });
            }
        } catch (err) {
            console.error(err);
            error.value = 'Erro ao gerar sugestões com IA.';
        } finally {
            isGenerating.value = false;
        }
    }

    async function toggleHabitCompletion(id: number) {
        try {
            const updateHabit = await habitService.toggleHabit(id);

            const index = habits.value.findIndex(h => h.id === id);
            if (index !== -1) {
                habits.value[index] = updateHabit;
            }
        } catch (err) {
            console.error(err);
            error.value = 'Erro ao atualizar hábito.';
        }
    }

    async function removeHabit(id: number) {
        if (!confirm('Tem certeza que deseja apagar este hábito?')) return;

        try {
            await habitService.deleteHabit(id);
            habits.value = habits.value.filter(h => h.id !== id);
        } catch (err) {
            console.error(err);
            error.value = 'Erro ao apagar Hábito.';
        }
    }

    return {
        habits,
        isLoading,
        isGenerating,
        error,
        fetchHabits,
        addHabit,
        generateHabitsFromGoal,
        toggleHabitCompletion,
        removeHabit
    };
});

