# Deploy SafeRoute AI

SafeRoute AI is packaged as one web service. The container serves both the dashboard and its prediction API on port `8001`.

## Local production-style run

```powershell
docker compose up --build -d
```

Open `http://localhost:8001`. Stop it with `docker compose down`.

## Deploy to a container host

1. Push this project to a Git repository.
2. In your host (Render, Railway, Fly.io, Azure Container Apps, Google Cloud Run, etc.), create a service from the repository and select the included `Dockerfile`.
3. Expose container port `8001` and configure the platform health check to `GET /health`.
4. Use the platform-provided HTTPS URL. No database, secret, or environment variables are needed for this demo.

## Important production changes

- The current model trains on synthetic data on every start. Replace `synthetic_records()` with an approved, versioned real dataset and load a validated model artifact instead.
- Put the service behind HTTPS, add access controls, rate limits, request logging, and monitoring before any public deployment.
- This prototype is not appropriate for operational traffic-safety decisions.
