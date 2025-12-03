import apiClient from './axiosInstance';
import type { Habit, CreateHabitDTO } from '@/types/habit';

export default {
    async getHabits(): Promise<Habit[]> {
        const response = await apiClient.get<Habit[]>('/habits/');
        return response.data;
    },

    async createHabit(data: CreateHabitDTO): Promise<Habit> {
        const response = await apiClient.post<Habit>('/habits/', data);
        return response.data;
    },

    async suggestHabits(goal: string): Promise<string[]> {
        const response = await apiClient.post<AIResponse>('/ai/suggest', { goal });
        return response.data.habits;
    },

    async deleteHabit(id: number): Promise<void> {
        await apiClient.delete(`/habits/${id}`);
    },

    async toggleHabit(id: number): Promise<Habit> {
        const response = await apiClient.post<Habit>(`/habits/${id}/toggle`);
        return response.data;
    }
};