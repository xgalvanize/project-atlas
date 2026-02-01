FROM node:20-alpine as build
WORKDIR /app
COPY package*.json ./
# Install build tools for native modules, then install deps (no --silent to show errors)
RUN apk add --no-cache python3 build-base git && npm ci
COPY . .
RUN npm run build

FROM nginx:stable-alpine
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
