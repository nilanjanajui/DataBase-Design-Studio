FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files first for Docker layer caching
COPY package.json package-lock.json ./
RUN npm install

# Copy public and src folders only (not node_modules or build)
COPY public/ ./public/
COPY src/ ./src/

RUN npm run build

# Stage 2 — Serve with Nginx
FROM nginx:alpine

COPY --from=builder /app/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]