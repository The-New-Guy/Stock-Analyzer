# Use an official Python runtime as a parent image
FROM node:17.9.0

# Set the working directory to /app
WORKDIR /app

# Copy the client directory contents into the container at /app
ADD . /app

# Install any needed packages
RUN npm install

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME frontend

# Start application
CMD npm run serve -- --port 80
