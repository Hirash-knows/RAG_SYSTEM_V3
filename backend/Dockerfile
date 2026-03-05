# Use official Node.js image
FROM node:20

# Set working directory inside container
WORKDIR /app

# Copy dependency files first (better caching)
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy backend source code
COPY . .

# Expose backend port
EXPOSE 3000

# Start backend server
CMD ["npm", "start"]
