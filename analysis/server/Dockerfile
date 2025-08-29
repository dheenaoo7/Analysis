FROM node:slim
WORKDIR /app
COPY . /app/
RUN npm install axios mysql2 node-cron playwright
EXPOSE 3001
CMD [ "node","server.js" ]
