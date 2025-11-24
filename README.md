# Three-Tier Web Application Using Docker

This project demonstrates a simple and clean implementation of a **three-tier web application**, with each component running inside its own Docker container.Its structure reflects a commonly used architectural pattern in modern software systems.

The three tiers are:

- **Frontend** — A static HTML page served through Nginx  
- **Backend** — A lightweight Flask API that retrieves data from the database  
- **Database** — A PostgreSQL instance storing a simple message

The purpose of this project is to show how data flows from the database → backend → frontend in a structured and modular environment.

---

## Project Structure
```bash
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
└── docker-compose.yml
```


Each folder contains all the required files for its corresponding layer.

---

## 1. Database Layer

The database layer initializes PostgreSQL using:

- **init.sql** — Creates a table and inserts an initial message  
- **Dockerfile** — Builds a PostgreSQL image and copies the initialization script into it

When the database container is started for the first time, PostgreSQL executes the SQL script automatically.

---

## 2. Backend Layer 
The backend is a small Flask application that:

1. Connects to the PostgreSQL database  
2. Reads the stored message  
3. Returns it as JSON to the frontend  

Main files:

- **app.py** — Contains the Flask API logic  
- **requirements.txt** — Defines Python dependencies  
- **Dockerfile** — Builds and runs the Flask server  

This layer acts as the bridge between the UI and the data storage.

---

## 3. Frontend Layer 

The frontend is a minimal HTML page that fetches and displays the message coming from the backend.

It includes:

- **index.html** — The user interface  
- **nginx.conf** — Nginx configuration for static hosting and reverse proxy  
- **Dockerfile** — Builds the Nginx image with the UI and configuration  

Nginx serves the page and forwards API requests to the backend container.

---

## Running the Application

From the project root folder:

```bash
docker compose build
docker compose up 
```

Once the stack is running, open the application in your browser:

http://localhost:8080


You should see the message retrieved from the PostgreSQL database.

## Stopping the Application
```bash
docker compose down
```
## Updating the Database Message
The SQL initialization file (init.sql) is executed only the first time the database container is created.
If you modify init.sql and want PostgreSQL to reload it, you must force a rebuild:
```bash
docker compose down
docker compose build --no-cache
docker compose up
```

This rebuilds PostgreSQL and re-applies the updated SQL script.



## Summary
This project demonstrates a clear and professional implementation of a three-tier architecture:

A dedicated UI layer

A separate API layer

An isolated database layer

Each tier is fully containerized and easy to maintain or extend.


