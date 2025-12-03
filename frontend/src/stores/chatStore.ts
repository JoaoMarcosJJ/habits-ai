import { defineStore } from 'pinia';
import { ref } from 'vue';
import apiClient from '@/api/axiosInstance';

export interface Message {
    role: 'user' | 'model';
    content: string;
}

export const useChatStore = defineStore('chat', () => {
    const messages = ref<Message[]>([
        { role: 'model', content: 'Olá! Eu sou o seu coach de hábitos. Como posso ajudar hoje?' }
    ]);
    const isLoading = ref(false);
    const isOpen = ref(false); // Controla se a janelinha está aberta

    async function sendMessage(text: string) {
        // Adiciona a mensagem do usuário na UI imediatamente
        messages.value.push({ role: 'user', content: text });
        isLoading.value = true;

        try {
            // Envia histórico para o backend
            const response = await apiClient.post('/ai/chat', { 
                messages: messages.value 
            });

            // Adiciona resposta da IA
            messages.value.push({ role: 'model', content: response.data.response });
        } catch (error) {
            console.error(error);
            messages.value.push({ role: 'model', content: 'Ops, tive um erro ao processar. Tente novamente.' });
        } finally {
            isLoading.value = false;
        }
    }

    function toggleChat() {
        isOpen.value = !isOpen.value;
    }

    return {
        messages,
        isLoading,
        isOpen,
        sendMessage,
        toggleChat
    };
});