FROM node:20-alpine

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm install

# Copy rest of the frontend
COPY . .

EXPOSE 5173

# Run Vite dev server and expose outside
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
