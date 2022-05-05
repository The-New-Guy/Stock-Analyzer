# Use an official Python runtime as a parent image.
FROM python:3.9.12

# Set the working directory to /server .
WORKDIR /server

# Need to install the updated gcc compiler for Pystan 3 needed by Prophet.
# Add the Debian source list.
RUN echo 'deb http://deb.debian.org/debian testing main' >> /etc/apt/sources.list

# Update the repos.
RUN apt-get update -y

# Install the latest gcc (required for PyStan).
RUN apt-get install -y gcc

# No need to install further packages so remove the lists to save space.
RUN rm -rf /var/lib/apt/lists/*

# Copy requirements file and install packages.
COPY requirements.txt /server
RUN pip3 install -r requirements.txt

# Copy application.
COPY . /server

# Make port available to the world outside this container.
EXPOSE 5000

# User provided environment variable. --build-arg ENVIRONMENT=production
ARG ENVIRONMENT

# Define environment variables.
# If ENVIRONMENT is null, set it to 'development' (or leave as is otherwise).
ENV ENVIRONMENT=${ENVIRONMENT:-development}

# Run app.py when the container launches.
CMD ["python", "app.py"]
