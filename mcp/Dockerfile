# Use a lightweight Node.js image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY tsconfig.json index.ts ./
COPY repo ./repo
COPY handlers ./handlers
COPY service ./service
COPY tools ./tools

# Build the project
RUN npm run build

# Expose the server via stdio (no network port needed for stdio transport)
# The default command runs the compiled JS
CMD ["node", "dist/index.js"]
