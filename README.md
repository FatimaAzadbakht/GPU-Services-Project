# GPU Quota Management System (GaaS)
A robust, high-performance RESTful API built with FastAPI designed to manage GPU resource allocation. This system provides a "GPU-as-a-Service" (GaaS) experience, allowing users to submit computational jobs while maintaining strict hour-based quotas.

---

# Key Features
- Secure Authentication: Implements JWT (JSON Web Tokens) with secure password hashing using the PBKDF2-SHA256 algorithm.

- Resource Quota Management: Every user starts with a predefined quota (e.g., 10 hours) which is automatically deducted upon job submission.

- Job Lifecycle Tracking: Jobs transition through states such as `PENDING`, `APPROVED`, `PROCESSING`, and `COMPLETED`.

- Role-Based Access Control (RBAC): Distinguishes between regular users and administrators for sensitive operations like job status updates.

- Automated Documentation: Interactive API documentation available via Swagger UI and ReDoc.

---

# Tech Stack 
Backend Framework: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.14 compatible)

ORM / Database: [SQLAlchemy](https://www.sqlalchemy.org/) with SQLite for local persistence.

Security: `passlib` for hashing and `python-jose` for JWT handling.

Deployment: [Docker](https://www.docker.com/) & Docker Compose for seamless environment replication.

---

# Project Structure
- main.py           Application entry point and API endpoints
- models.py         Database schema and SQLAlchemy models
- auth.py           Security logic, hashing, and JWT utilities
- database.py       Database engine and session configuration
- requirements.txt  Project dependencies
- .gitignore        Files to be ignored by Git

---

# Getting Started
#### 1. Prerequisites
Ensure you have Python 3.14+ installed.

#### 2. Installation
Clone the repository and install dependencies:
```bash
pip install -r requirements.txt
```

#### 3. Running the Server
Start the FastAPI server using Uvicorn:
```bash
uvicorn main:app --reload
```
The API will be live at `http://localhost:8000`.

#### 4. Interactive API Docs
Once the server is running, explore the API endpoints:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

# Docker Deployment
To run the entire stack in a containerized environment:
```bash
docker-compose up --build
```

---

# Security & Logic Flow
1. Registration: Users register and receive an initial GPU quota.

2. Job Submission: The system checks if the requested hours exceed the user's current quota. If insufficient, a `400 Bad Request` is returned.

3. Quota Deduction: Upon valid submission, hours are subtracted immediately to prevent over-allocation.

4. Admin Review: Only users with the `admin` role can update job statuses to `APPROVED` or `COMPLETED`.