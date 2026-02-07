FROM node:20-alpine as build
WORKDIR /app
COPY package*.json ./
# Install build tools for native modules, then install deps (no --silent to show errors)
RUN apk add --no-cache python3 build-base git && npm install
COPY . .
RUN npm run build

FROM nginx:stable-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
