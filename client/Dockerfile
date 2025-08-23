FROM node:22-alpine as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM alpine:latest
WORKDIR /app
COPY --from=build /app/dist ./dist

CMD ["tail", "-f", "/dev/null"] 