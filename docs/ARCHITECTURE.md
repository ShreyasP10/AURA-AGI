# Kiosk Agent Platform Architecture
## Purpose
This platform replaces the legacy console-loop runtime with a lightweight, Docker-hosted service. A Galaxy Book running Windows 10 remains a kiosk client: it renders the interface, captures explicit microphone/webcam input, plays speech, and presents approvals. All model calls, search retrieval, memory, integration logic, and optional image analysis run on the server.
## Deployment Shape
| Component | Location | Responsibility |
|---|---|---|
| `agent-server` | Docker host | FastAPI API, Ollama provider adapter, bounded task planner, SQLite memory, action rules, streamed answers, static kiosk assets. |
| `searxng` | Docker host | Aggregated web-search JSON endpoint. |
| Ollama | Docker host or host machine | Configurable local text/vision model endpoint. |
| Google Drive | Google account | Optional OAuth-authorized backup, selected per-person files, and document import source; it is never the compute host. |
| Galaxy Book kiosk | Windows 10 tablet | Browser-only display, microphone, webcam, speakers, and owner approval surface. |
## Agent Boundaries
| Action category | Default policy |
|---|---|
| Search, recall, document retrieval, local memory | Allowed within the active profile and configured sources. |
| Compose message or booking | Produce draft, then require spoken or on-screen confirmation before submission. |
| File transfer, location share, smart-device control | Available only through named owner-managed rules with destination/device allowlists, expiry, status history, and a global stop switch. |
| Webcam, microphone, face/profile enrollment | Explicit browser permission, visible in-app state, opt-in per feature, and owner-managed deletion. |
| Credentials, payments, passwords, destructive operations, security settings | Not automated by the agent. |
## Service Layout
```text
agent_server/
  app/
    main.py                 FastAPI application and static kiosk delivery
    config.py               Environment-driven configuration
    db.py                   SQLite schema and data access
    models.py               API request/response types
    adapters/               Ollama, SearXNG, Google Drive, device adapters
    services/               Agent, memory, search, actions, profiles, policy
    static/                 Zero-build HTML/CSS/JavaScript kiosk client
  tests/                    Unit and API smoke tests
```
