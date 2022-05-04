# Use an official Python runtime as a parent image
FROM node

# Set the working directory to /client
WORKDIR /app

# Copy the client directory contents into the container at /client
ADD . /app

# Install any needed packages specified in requirements.txt
RUN npm install

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME frontend

# Start application
CMD ng serve --host 0.0.0.0 --port 80
