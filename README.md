# Three-Tier Web Application Using Docker and Kubernetes

This project demonstrates a simple and clean implementation of a **three-tier web application**, with each component running inside its own Docker container. The structure reflects a commonly used architectural pattern in modern software systems.

The three tiers are:

- **Frontend** — A static HTML page served through Nginx  
- **Backend** — A lightweight Flask API that retrieves data from the database  
- **Database** — A PostgreSQL instance storing a simple message

The purpose of this project is to show how data flows from the database → backend → frontend in a structured and modular environment.

---

## Project Structure
```
three-tier-app/
│
├── frontend/
│ ├── index.html
│ ├── nginx.conf
│ └── Dockerfile
│
├── backend/
│ ├── app.py
│ ├── requirements.txt
│ └── Dockerfile
│
├── db/
│ ├── init.sql
│ └── Dockerfile
│
├── k8s/
│ └── three-tier-all.yaml
│
└── docker-compose.yml
```

Each folder contains all the required files for its corresponding layer.

---

# Docker Deployment

## 1. Database Layer

The database layer initializes PostgreSQL using:

- **init.sql** — Creates a table and inserts an initial message  
- **Dockerfile** — Builds a PostgreSQL image and copies the initialization script  

When the database container is started for the first time, PostgreSQL executes the SQL script automatically.

---

## 2. Backend Layer 

The backend is a small Flask application that:

1. Connects to the PostgreSQL database  
2. Reads the stored data  
3. Returns it as JSON to the frontend  

Main files:

- **app.py** — Contains the Flask API logic  
- **requirements.txt** — Python dependencies  
- **Dockerfile** — Builds and runs the Flask server  

This layer acts as the bridge between the UI and the data storage.

---

## 3. Frontend Layer 

The frontend is a minimal HTML interface that fetches and displays data coming from the backend.

It includes:

- **index.html** — The user interface  
- **nginx.conf** — Nginx configuration  
- **Dockerfile** — Builds the Nginx image  

Nginx serves the static files and forwards API requests to the backend container.

---

# Running the Application with Docker

From the project root:

```
docker compose build
docker compose up
```

Open the application:

```
http://localhost:8080
```

Stopping the application:

```
docker compose down
```

---

# Updating the Database Message

`init.sql` runs **only on first creation** of the database container.  
To re-apply modifications, you must rebuild PostgreSQL:

```
docker compose down
docker compose build --no-cache
docker compose up
```

---

# Kubernetes Deployment 

The project also includes a full Kubernetes setup replicating the same three-tier architecture.  
Kubernetes manages the application's lifecycle using declarative configuration and ensures each component is running as defined.

### Files:
```
k8s/three-tier-all.yaml
```

### This file defines:

- **Deployments** for:
  - Database (PostgreSQL)
  - Backend (Flask API)
  - Frontend (Nginx)

- **Services** for:
  - `db` → ClusterIP (internal communication)
  - `backend` → ClusterIP (internal API access)
  - `three-tier-frontend` → NodePort (external access)

### Running the Kubernetes Version

1. Ensure Kubernetes is enabled (Docker Desktop → Settings → Kubernetes).
2. Apply the configuration:

```
kubectl apply -f k8s/three-tier-all.yaml
```

3. Check running pods:

```
kubectl get pods
```

4. Access the application through the NodePort service:

```
http://localhost:30080
```

### Viewing the Database Inside Kubernetes

To inspect the PostgreSQL database:

```
kubectl exec -it <db-pod-name> -- psql -U three_tier_user -d three_tier_db
```

Then:

```
SELECT * FROM tasks;
```

Each environment (Docker and Kubernetes) has its **own** isolated database instance.

---

# Summary

This project demonstrates a clear and professional implementation of a distributed three-tier architecture:

- A dedicated **UI layer**  
- A separate **API layer**  
- An isolated **database layer**  

Both **Docker Compose** and **Kubernetes** deployments are supported, showing the evolution from simple containerization to full orchestration. Each tier is fully modular, making the system easy to maintain, scale, or extend.
