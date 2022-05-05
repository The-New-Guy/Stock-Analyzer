# Use an official Node.js runtime as a parent image.
FROM node:17.9.0

# Set the working directory to /client .
WORKDIR /client

# Copy the client directory contents into the container at /client .
ADD . /client

# Install any needed packages.
RUN npm install

# Make port available to the world outside this container.
EXPOSE 80

# User provided environment variable. --build-arg ENVIRONMENT=production
ARG ENVIRONMENT=development

# Set correct config file and remove the others.
RUN if [ "$ENVIRONMENT" = "development" ]; \
    then rm src/config.json && mv src/config-dev.json src/config.json; \
    else rm src/config-dev.json; \
fi

# Define environment variables.
# If ENVIRONMENT is null, set it to 'development' (or leave as is otherwise).
ENV ENVIRONMENT=${ENVIRONMENT:-development}

# Start application.
CMD npm run serve -- --port 80
