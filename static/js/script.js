document.addEventListener('DOMContentLoaded', () => {
    
    const habitForm = document.getElementById('new-habit-form');
    const habitInput = document.getElementById('habit-input');
    const habitList = document.getElementById('habit-list');
    const emptyState = document.getElementById('empty-state');
    
    const geminiSuggestBtn = document.getElementById('gemini-suggest-btn');
    const apiLoading = document.getElementById('api-loading');
    
    const errorModal = document.getElementById('error-modal');
    const errorMessage = document.getElementById('error-message');
    const closeModalBtn = document.getElementById('close-modal-btn');

    let habits = []; 
    let chartInstances = {};

    // --- Funções de UI (Modal e Loading) ---

    function showModal(message) {
        errorMessage.textContent = message || "Não foi possível processar sua solicitação.";
        errorModal.classList.remove('hidden');
    }

    function hideModal() {
        errorModal.classList.add('hidden');
    }

    function showLoading() {
        apiLoading.classList.remove('hidden');
        geminiSuggestBtn.disabled = true;
        geminiSuggestBtn.classList.add('btn-secondary:disabled'); 
    }

    function hideLoading() {
        apiLoading.classList.add('hidden');
        geminiSuggestBtn.disabled = false;
        geminiSuggestBtn.classList.remove('btn-secondary:disabled');
    }

    // --- Funções Principais de Dados (Fetch API) ---

    /**
     * Carrega os hábitos do backend
     */
    async function loadHabits() {
        try {
            const response = await fetch('/api/habits');
            if (!response.ok) {
                throw new Error(`Erro ao carregar hábitos: ${response.statusText}`);
            }
            habits = await response.json();
            renderHabits();
        } catch (error) {
            console.error(error);
            showModal(error.message);
        }
    }

    /* Renderiza a lista de hábitos na tela */
    function renderHabits() {
        // Limpa a lista atual
        habitList.innerHTML = '';
        
        // Destrói gráficos antigos para evitar memory leak
        Object.values(chartInstances).forEach(chart => chart.destroy());
        chartInstances = {};

        if (habits.length === 0) {
            habitList.appendChild(emptyState);
        } else {
            habits.forEach(habit => {
                const habitElement = createHabitElement(habit);
                habitList.appendChild(habitElement);
                
                // Renderiza o gráfico para este hábito
                renderChart(habit);
            });
        }
    }

    /* Cria o elemento HTML para um único hábito */
    function createHabitElement(habit) {
        const element = document.createElement('div');
        element.className = 'habit-card';
        
        const todayStr = getTodayString();
        const isCompleted = habit.completed_dates.includes(todayStr);

        // Lógica de cálculo (Streak, Porcentagem)
        // Estas funções são idênticas às da versão localStorage
        const streak = calculateStreak(habit);
        const percentage = calculateSuccessPercentage(habit);

        element.innerHTML = `
            <!-- Linha 1: Nome e Botão de Remover -->
            <div class="habit-row">
                <span class="habit-name">${habit.name}</span>
                <button class="habit-delete-btn" data-id="${habit.id}" title="Remover hábito">
                    Remover
                </button>
            </div>

            <!-- Linha 2: Estatísticas -->
            <div class="habit-stats">
                <div class="stat-item">
                    <span class="stat-icon">🔥</span>
                    <span class="stat-value">${streak}</span>
                    <span class="stat-label">dias</span>
                </div>
                <div class="stat-item">
                    <span class="stat-icon">📊</span>
                    <span class="stat-value">${percentage}%</span>
                    <span class="stat-label">sucesso</span>
                </div>
            </div>

            <!-- Linha 3: Gráfico (Últimos 7 dias) -->
            <div class="chart-container">
                <canvas id="chart-${habit.id}"></canvas>
            </div>

            <!-- Linha 4: Botão de Ação -->
            <button 
                class="btn btn-complete"
                data-id="${habit.id}"
                ${isCompleted ? 'disabled' : ''}
            >
                ${isCompleted ? 'Feito ✔' : 'Marcar Hoje'}
            </button>
        `;

        // Adiciona listeners para os botões
        element.querySelector('.habit-delete-btn').addEventListener('click', () => handleDelete(habit.id));
        element.querySelector('.btn-complete').addEventListener('click', () => handleToggleComplete(habit.id));

        return element;
    }
    
    /**
     * Renderiza o gráfico de 7 dias para um hábito
     */
    function renderChart(habit) {
        const ctx = document.getElementById(`chart-${habit.id}`).getContext('2d');
        if (!ctx) return;

        const { labels, data } = getChartData(habit, 7); // Pegar dados dos últimos 7 dias

        if (chartInstances[habit.id]) {
            chartInstances[habit.id].destroy();
        }

        chartInstances[habit.id] = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Concluído',
                    data: data,
                    backgroundColor: 'rgba(34, 197, 94, 0.6)',
                    borderColor: 'rgba(34, 197, 94, 1)',
                    borderWidth: 1,
                    borderRadius: 4,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: { enabled: false }
                },
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 1,
                        display: false
                    },
                    x: {
                        ticks: {
                            font: { size: 10 }
                        }
                    }
                }
            }
        });
    }

    // --- Handlers de Eventos (Fetch API) ---

    /**
     * Adiciona um novo hábito (via formulário)
     */
    async function handleFormSubmit(e) {
        e.preventDefault();
        const habitName = habitInput.value.trim();
        
        if (habitName) {
            try {
                const response = await fetch('/api/habits', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ name: habitName })
                });

                if (!response.ok) {
                    throw new Error('Não foi possível adicionar o hábito.');
                }
                
                habitInput.value = '';
                await loadHabits(); // Recarrega a lista do servidor

            } catch (error) {
                console.error(error);
                showModal(error.message);
            }
        }
    }
    
    /**
     * Handler: Botão Gemini para sugestões
     */
    async function handleGeminiSuggest() {
        const goal = habitInput.value.trim();
        if (!goal) {
            showModal("Por favor, digite uma meta ou um hábito primeiro.");
            return;
        }

        showLoading();

        try {
            // Chama o *nosso* backend, que por sua vez chama o Gemini
            const response = await fetch('/api/suggest', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ goal: goal })
            });
            
            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.error || "Erro ao gerar sugestões.");
            }

            // O backend já adicionou os hábitos no DB.
            // Nós apenas precisamos recarregar a lista.
            await loadHabits();
            habitInput.value = ''; // Limpa o input

        } catch (error) {
            console.error("Erro ao chamar a API de sugestão:", error);
            showModal(`Erro ao contatar o assistente: ${error.message}`);
        } finally {
            hideLoading();
        }
    }

    /**
     * Marca um hábito como completo/incompleto para hoje
     */
    async function handleToggleComplete(id) {
        const todayStr = getTodayString();
        try {
            const response = await fetch(`/api/habits/${id}/toggle`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ date: todayStr })
            });

            if (!response.ok) {
                throw new Error('Não foi possível atualizar o hábito.');
            }
            
            // Recarrega tudo para simplicidade.
            // Uma otimização seria apenas atualizar o 'habits' local.
            await loadHabits(); 

        } catch (error) {
            console.error(error);
            showModal(error.message);
        }
    }

    /**
     * Deleta um hábito
     */
    async function handleDelete(id) {
        // Futuramente, adicionar um modal de confirmação aqui.
        try {
            const response = await fetch(`/api/habits/${id}`, {
                method: 'DELETE'
            });

            if (!response.ok) {
                throw new Error('Não foi possível deletar o hábito.');
            }

            await loadHabits(); // Recarrega a lista

        } catch (error) {
            console.error(error);
            showModal(error.message);
        }
    }

    // --- Funções Utilitárias (Lógica Pura - Idênticas) ---

    function getTodayString() {
        return new Date().toISOString().split('T')[0];
    }
    
    function getDateString(date) {
        return date.toISOString().split('T')[0];
    }

    function calculateStreak(habit) {
        let streak = 0;
        // Agora acessamos 'completed_dates'
        const sortedDates = [...habit.completed_dates].sort().reverse();
        if (sortedDates.length === 0) return 0;
        
        const checkDate = new Date();
        
        const todayStr = getDateString(checkDate);
        checkDate.setDate(checkDate.getDate() - 1);
        const yesterdayStr = getDateString(checkDate);
        
        if (sortedDates[0] !== todayStr && sortedDates[0] !== yesterdayStr) {
            return 0;
        }
        
        checkDate.setTime(new Date(sortedDates[0]).getTime());

        for (const dateStr of sortedDates) {
            if (dateStr === getDateString(checkDate)) {
                streak++;
                checkDate.setDate(checkDate.getDate() - 1);
            } else {
                break;
            }
        }
        return streak;
    }

    function calculateSuccessPercentage(habit) {
        // Agora acessamos 'completed_dates' e 'created_at'
        if (habit.completed_dates.length === 0) return 0;
        
        const startDate = new Date(habit.created_at);
        const today = new Date();
        
        const diffTime = Math.abs(today - startDate);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1;

        const totalCompletions = habit.completed_dates.length;
        
        const percentage = (totalCompletions / diffDays) * 100;
        return Math.round(percentage);
    }
    
    function getChartData(habit, days) {
        const labels = [];
        const data = [];
        const checkDate = new Date();

        for (let i = 0; i < days; i++) {
            const dateStr = getDateString(checkDate);
            labels.push(checkDate.toLocaleDateString('pt-BR', { weekday: 'short' }).substring(0, 3));
            data.push(habit.completed_dates.includes(dateStr) ? 1 : 0);
            checkDate.setDate(checkDate.getDate() - 1);
        }
        return { labels: labels.reverse(), data: data.reverse() };
    }

    // --- Inicialização ---
    habitForm.addEventListener('submit', handleFormSubmit);
    geminiSuggestBtn.addEventListener('click', handleGeminiSuggest);
    closeModalBtn.addEventListener('click', hideModal);

    // Carrega os dados iniciais do backend ao iniciar o app
    loadHabits();
});