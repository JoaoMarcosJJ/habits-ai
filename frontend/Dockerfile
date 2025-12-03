# Usar imagem leve do Node
FROM node:20-alpine

WORKDIR /app

# Copiar arquivos de dependência
COPY package*.json ./

# Instalar dependências
RUN npm install

# Copiar o resto do código
COPY . .

# Expor a porta do Vite
EXPOSE 5173

# Comando de desenvolvimento
CMD ["npm", "run", "dev", "--", "--host"]