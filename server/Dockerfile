# Use an official Python runtime as a parent image
FROM python:3.9.12

# Set the working directory to /app
WORKDIR /app

# Need to install the updated gcc compiler for Pystan 3
# Add the Debian source list
RUN echo 'deb http://deb.debian.org/debian testing main' >> /etc/apt/sources.list

# Update the repos
RUN apt-get update -y

# Install the latest gcc (required for PyStan)
RUN apt-get install -y gcc

# No need to install further packages so remove the lists to save space
RUN rm -rf /var/lib/apt/lists/*

# Copy and install the rest of the requirements.
COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY . /app

# # Copy the server directory contents into the container at /app
# ADD ./server /app

# # Install any needed packages specified in requirements.txt
# RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV NAME backend

# Run app.py when the container launches
CMD ["python", "app.py"]
