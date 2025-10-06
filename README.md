## Running the Project with Docker

This project is containerized using Docker and Docker Compose, with dedicated services for the frontend (React), inventory (FastAPI), and payment (FastAPI with Gunicorn). Below are the specific instructions and requirements for running the project:

### Project-Specific Docker Requirements

- **Frontend**
  - Node.js version: `22.13.1-slim` (set via `NODE_VERSION` ARG)
  - Serves static files using the `serve` package
  - Exposes port **3000**

- **Inventory**
  - Python version: `3.11-slim`
  - Uses a virtual environment for dependencies (from `requirements.txt`)
  - Runs FastAPI app with Uvicorn
  - Exposes port **8000**

- **Payment**
  - Python version: `3.13-slim`
  - Uses a virtual environment for dependencies (from `requirements.txt`)
  - Runs FastAPI app with Gunicorn/Uvicorn worker
  - Exposes port **8001**

### Environment Variables

- Each service supports an `.env` file for environment variables (see commented `env_file` lines in `docker-compose.yaml`).
- If you have environment-specific settings, place them in the respective `.env` files (`./frontend/.env`, `./inventory/.env`, `./payment/.env`) and uncomment the `env_file` lines in the compose file.

### Build and Run Instructions

1. **Ensure Docker and Docker Compose are installed.**
2. **Build and start all services:**
   ```sh
   docker compose up --build
   ```
   This will build images for each service and start them with the following port mappings:
   - Frontend: [http://localhost:3000](http://localhost:3000)
   - Inventory API: [http://localhost:8000](http://localhost:8000)
   - Payment API: [http://localhost:8001](http://localhost:8001)

3. **Custom Commands:**
   - To run the Python consumers instead of the API servers, override the default command, e.g.:
     ```sh
     docker compose run py-inventory python consumer.py
     docker compose run py-payment python consumer.py
     ```

### Special Configuration

- All services run as non-root users for improved security.
- The Dockerfiles use multi-stage builds for smaller, production-ready images.
- The `appnet` bridge network is used for inter-service communication.
- The `.dockerignore` files should exclude `.env`, `.git`, `venv/`, `__pycache__/`, and other build artifacts for efficient builds.

---

*This section was updated to reflect the current Docker-based setup for the project. Please ensure your local `.env` files are configured as needed and uncomment the relevant lines in `docker-compose.yaml` if you wish to use them.*
