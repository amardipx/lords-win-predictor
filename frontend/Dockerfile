# ============================
# Stage 1 — Build the frontend
# ============================
FROM node:20-alpine AS build

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy all frontend files
COPY . .

# Inject production environment variables
# This ensures Vite uses the correct API URL during build
COPY .env.production .env

# Build static assets
RUN npm run build


# =====================================
# Stage 2 — Serve the production build
# =====================================
FROM node:20-alpine AS prod

WORKDIR /app

# Install a lightweight static file server
RUN npm install -g serve

# Copy built frontend from previous stage
COPY --from=build /app/dist ./dist

# Expose port 8080 for Railway / Docker
EXPOSE 8080

# Run the static server
CMD ["serve", "-s", "dist", "-l", "8080"]
