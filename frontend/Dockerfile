# frontend/Dockerfile
FROM node:18-alpine

WORKDIR /app

COPY package*.json .  
RUN npm ci

COPY . .
RUN npm run build

# serve with a simple static server
RUN npm install -g serve
CMD ["serve", "-s", "dist", "-l", "3000"]
