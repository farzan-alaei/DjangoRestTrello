# Use the Node 20 slim image
FROM node:20-slim

# Set the working directory to /app
WORKDIR /app

# Copy the package.json and package-lock.json files to the container
COPY package*.json ./
COPY svelte.config.js ./
COPY vite.config.js ./
RUN npm ci

# Copy the rest of the application code to the container
COPY . .

EXPOSE 8080


CMD ["npm", "run", "dev"]
