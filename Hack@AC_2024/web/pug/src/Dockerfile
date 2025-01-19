FROM node:20-alpine3.18

WORKDIR /app

COPY . /app
RUN chmod -R 755 /app

RUN npm install

EXPOSE 3000

USER node
CMD ["node", "index.js"]
