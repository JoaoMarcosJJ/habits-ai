export interface Habit {
    id: number;
    name: string;
    description?: string | null;
    created_at: string;
    is_active: boolean;
    logs: HabitLog[];
}

// Interface para criar um novo 
export interface CreateHabitDTO {
    name: string;
    description?: string;
}

export interface HabitLog {
    id: number;
    completed_date: String;
}

