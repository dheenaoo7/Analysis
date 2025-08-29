FROM mcr.microsoft.com/playwright:v1.47.2-jammy

WORKDIR /app
COPY . /app/

RUN npm install axios mysql2 node-cron

EXPOSE 3001
CMD ["node","server.js"]
