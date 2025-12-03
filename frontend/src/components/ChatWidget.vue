<script setup lang="ts">
import { ref, nextTick, watch } from 'vue';
import { useChatStore } from '@/stores/chatStore';
import { MessageCircle, X, Send } from 'lucide-vue-next';
import { marked } from 'marked';

const chatStore = useChatStore();
const userInput = ref('');
const messagesContainer = ref<HTMLElement | null>(null);

// Rolar para baixo automaticamente quando chega mensagem nova
watch(() => chatStore.messages.length, () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
    }
  });
});

const handleSend = () => {
  if (!userInput.value.trim()) return;
  chatStore.sendMessage(userInput.value);
  userInput.value = '';
};

const renderMarkdown = (text: string) => {
  return marked.parse(text);
};
</script>

<template>
  <div class="chat-wrapper">
    <button class="chat-toggle-btn" @click="chatStore.toggleChat">
      <X v-if="chatStore.isOpen" />
      <MessageCircle v-else />
    </button>

    <transition name="slide-up">
      <div v-if="chatStore.isOpen" class="chat-window">
        <div class="chat-header">
          <h3>Coach IA 🤖</h3>
        </div>

        <div class="chat-messages" ref="messagesContainer">
          <div 
            v-for="(msg, index) in chatStore.messages" 
            :key="index"
            class="message-bubble"
            :class="msg.role === 'user' ? 'user-msg' : 'ai-msg'"
          >
            <div v-if="msg.role === 'model'" v-html="renderMarkdown(msg.content)"></div>
            <div v-else>{{ msg.content }}</div>
          </div>
        </div>

        <div class="chat-input-area">
          <input 
            v-model="userInput" 
            @keyup.enter="handleSend"
            placeholder="Pergunte algo..."
            :disabled="chatStore.isLoading"
          />
          <button @click="handleSend" :disabled="chatStore.isLoading">
            <Send :size="16" />
          </button>
        </div>
      </div>
    </transition>
  </div>
</template>

<style scoped>
/* --- Layout do Botão Flutuante --- */
.chat-wrapper {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.chat-toggle-btn {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background-color: #42b983;
  color: white;
  border: none;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s;
}

.chat-toggle-btn:hover {
  transform: scale(1.1);
}

.chat-window {
  width: 320px;
  height: 450px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 5px 20px rgba(0,0,0,0.15);
  display: flex;
  flex-direction: column;
  margin-bottom: 16px;
  overflow: hidden;
  border: 1px solid #eee;
}

.chat-header {
  background-color: #42b983;
  color: white;
  padding: 12px;
  font-weight: bold;
  display: flex;
  align-items: center;
}

.chat-header h3 { margin: 0; font-size: 1rem; }

.chat-messages {
  flex: 1;
  padding: 12px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
  background-color: #f9f9f9;
}

.message-bubble {
  max-width: 80%;
  padding: 8px 12px;
  border-radius: 12px;
  font-size: 0.9rem;
  line-height: 1.4;
  word-wrap: break-word;
}

.message-bubble :deep(p) {
  margin: 0 0 8px 0; 
}

.message-bubble :deep(p:last-child) {
  margin-bottom: 0;
}

.message-bubble :deep(strong) {
  font-weight: 700;
  color: inherit; 
}

.message-bubble :deep(ul), .message-bubble :deep(ol) {
  margin: 4px 0 8px 20px; 
  padding: 0;
}

.message-bubble :deep(li) {
  margin-bottom: 4px;
}

.user-msg {
  align-self: flex-end;
  background-color: #42b983;
  color: white;
  border-bottom-right-radius: 2px;
}

.ai-msg {
  align-self: flex-start;
  background-color: #e5e7eb;
  color: #374151; 
  border-bottom-left-radius: 2px;
}


.typing { 
  font-style: italic; 
  color: #666; 
  font-size: 0.8rem; 
}

.chat-input-area {
  padding: 10px;
  border-top: 1px solid #eee;
  display: flex;
  gap: 8px;
  background: white;
  align-items: center;
}

.chat-input-area input {
  flex: 1;
  padding: 10px 14px;
  border: 1px solid #ccc !important;
  border-radius: 20px;
  outline: none;
  font-size: 0.95rem;
  min-height: 40px; 
  background-color: #ffffff !important;
  color: #1f2937 !important; 
  caret-color: #1f2937 !important; 
  -webkit-text-fill-color: #1f2937 !important; 
  
  box-shadow: inset 0 1px 2px rgba(0,0,0,0.05);
}

.chat-input-area input::placeholder {
  color: #9ca3af !important;
  -webkit-text-fill-color: #9ca3af !important;
  opacity: 1;
}

.chat-input-area input:focus {
  border-color: #42b983 !important;
  background-color: #ffffff !important;
  box-shadow: 0 0 0 2px rgba(66, 185, 131, 0.2);
}

.chat-input-area button {
  background: none;
  border: none;
  color: #42b983;
  cursor: pointer;
  padding: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.1s;
}

.chat-input-area button:active {
  transform: scale(0.9);
}

.chat-input-area button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.5, 1);
}

.slide-up-enter-from,
.slide-up-leave-to {
  opacity: 0;
  transform: translateY(20px) scale(0.95);
}
</style>