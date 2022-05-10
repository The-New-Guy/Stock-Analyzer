# Stock-Analyzer

A simple stock price analyzer tool built on Vue.js, Bootstrap, and a Flask backend.

## Developer Setup

### Using Containers

First you must have Docker installed. I use Chocolatey. This must be done from an administrative console.

```powershell
# Install chocolatey.
choco install docker-desktop

# Grant regular user account access to docker. Re-login.
Add-LocalGroupMember -Group 'docker-users' -Member domain\username
```

Now build the Docker image in the default mode which is `development` mode for this project. Then start the containers.

```powershell
# Build container images.
docker-compose build

# Bring up containers.
docker-compose up

##--OR--##

# Build container images and bring them up.
docker-compose up --build
```

This will launch a backend container running Python/Flask and a frontend running Node.js and Vue.js webpack. Both containers will be accessible on the localhost via your browser.

- <http://localhost> - Main frontend website.
- <http://localhost:5000/v1/client/data> - Backend API.
