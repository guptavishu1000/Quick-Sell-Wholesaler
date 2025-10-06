# frontend/Dockerfile
FROM node:16-alpine

# Set the working directory
WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the application files
COPY . .

# Build the React application
RUN npm run build

# Install 'serve' to act as a simple static server
RUN npm install -g serve

# Expose the port 'serve' will run on
EXPOSE 3000

# Command to run the app
CMD ["serve", "-s", "build", "-l", "3000"]