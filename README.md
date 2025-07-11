# 🚀 Dangerous Goods Service

This service provides an API for managing dangerous goods information, including UN codes, classification, packing groups, special provisions, and more.

---

## 📋 Table of Contents

1. [Prerequisites](#-prerequisites)
2. [Basic Docker Compose Commands](#-basic-docker-compose-commands)

   * [Build & Start Services](#1-build--start-services)
   * [Start Services](#2-start-services)
   * [View Logs](#3-view-logs)
   * [List Running Containers](#4-list-running-containers)
   * [Execute Commands Inside a Container](#5-execute-commands-inside-a-container)
   * [Stop Services](#6-stop-services)
   * [Restart Services](#7-restart-services)
   * [Remove Containers, Networks & Volumes](#8-remove-containers-networks--volumes)
   * [Rebuild a Single Service](#9-rebuild-a-single-service)
3. [Development Workflow](#-development-workflow)
4. [Troubleshooting](#-troubleshooting)

---

## 🔧 Prerequisites

* [Docker](https://www.docker.com/)
* [Docker Compose](https://docs.docker.com/compose/)
* \[Optional] Python 3.10-slim-bullseye (for local development without Docker)

---

## ⚙️ Basic Docker Compose Commands

The following commands help you manage the service using Docker Compose.

### 1. Build & Start Services

Build images (after modifying Dockerfile or dependencies) and start all containers in detached mode:

```bash
# Build images and start all containers
docker-compose up -d --build
```

### 2. Start Services

Start containers based on existing images (skip rebuild):

```bash
# Start all containers in detached mode
docker-compose up -d
```

### 3. View Logs

Follow logs for all services or a specific service:

```bash
# Follow logs for all services
docker-compose logs -f

# Follow logs for the Django web service only
docker-compose logs -f web
```

### 4. List Running Containers

Show status, ports, and uptime of all services:

```bash
docker-compose ps
```

### 5. Execute Commands Inside a Container

Run a shell or Django management commands inside the `web` container:

```bash
# Open a bash shell in the Django container
docker-compose exec web bash

# Apply migrations inside the Django container
docker-compose exec web python manage.py migrate
```

### 6. Stop Services

Stop all running containers:

```bash
docker-compose stop
```

### 7. Restart Services

Restart all containers:

```bash
docker-compose restart
```

### 8. Remove Containers, Networks & Volumes

Bring down containers and networks, optionally removing volumes:

```bash
# Stop and remove containers & networks (keep volumes)
docker-compose down

# Stop and remove everything, including volumes
docker-compose down -v
```

### 9. Rebuild a Single Service

Rebuild and restart only the `web` service:

```bash
docker-compose up -d --build web
```

---

## 🚀 Development Workflow

1. **Clone the repository**

   ```bash
   git clone <repository_url>
   cd dangerous-goods-service
   ```
2. **Build and start services**

   ```bash
   docker-compose up -d --build
   ```
3. **Apply database migrations**

   ```bash
   docker-compose exec web python manage.py migrate
   ```
4. **(Optional) Create a superuser**

   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```
5. **Access the API**
   Open your browser at:

   ```

   http://localhost:8000/
   ```

---

## 🎉 Troubleshooting

* **Dependencies changed**: If you update `requirements.txt` or `Dockerfile`, rebuild with:

  ```bash
  docker-compose up -d --build
  ```
* **Stale volumes**: To clear cached data (e.g., Redis), run:

  ```bash
  docker-compose down -v
  docker-compose up -d
  ```
* **Container issues**: Check individual logs:

  ```bash
  docker-compose logs web    # Django service
  docker-compose logs celery # Celery worker
  ```

---
