import axios from 'axios';

const apiClient = axios.create({
    baseURL: '/api', // O Vite faz o proxy disto para o Backend
    headers: {
        'Content-Type': 'application/json',
    },
});

export default apiClient;