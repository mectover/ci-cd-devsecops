# Use the official Nginx image as the base image
FROM nginx:latest

# Copy the Nginx configuration file to the container

# Create a directory to store your HTML files
RUN mkdir -p /usr/share/nginx/html

# Copy your HTML files to the container
COPY image-process.html /usr/share/nginx/html/
COPY joblists.html /usr/share/nginx/html/

# Expose port 80
EXPOSE 80

# Start Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]
