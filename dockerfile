# Use a Python base image
FROM python:3.9-slim as backend-build

WORKDIR /app

# Copy the backend code
COPY ./server /app

# Install Python dependencies
RUN pip install Flask Flask-CORS requests

# Use a Node.js base image for frontend
FROM node:16 as frontend-build

WORKDIR /app

# Copy the frontend code
COPY ./frontend /app

# Install frontend dependencies and build
RUN npm install
RUN npm run build

# Use Nginx for serving
FROM nginx:alpine

# Copy the backend from the backend-build stage
COPY --from=backend-build /app /app

# Copy the frontend build from the frontend-build stage
COPY --from=frontend-build /app/dist /usr/share/nginx/html

# Copy the nginx configuration
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

# Expose the port nginx is running on
EXPOSE 80

# Set the command to run your application
CMD ["nginx", "-g", "daemon off;"]
