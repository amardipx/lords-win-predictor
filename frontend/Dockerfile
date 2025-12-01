FROM node:20-alpine AS build

WORKDIR /app
COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# ---

FROM node:20-alpine AS prod

WORKDIR /app

# Install a tiny static server
RUN npm install -g serve

# Copy build output from the builder stage
COPY --from=build /app/dist ./dist

EXPOSE 8080

# Serve the built frontend
CMD ["serve", "-s", "dist", "-l", "8080"]
