# Assignment 2 — Traffic Visualisation

Real-time visualisation of network traffic on an interactive 3D globe.

## How to run

Requirements: Docker Desktop

```bash
git clone https://github.com/mawk8/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
docker compose up --build
```

Open **http://localhost:5000** in your browser.

The sender script will start automatically once Flask is ready and begin streaming packets to the globe in real time.
