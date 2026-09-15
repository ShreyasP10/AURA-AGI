# Owner Rollout Plan
| Stage | Goal | Owner action | Success condition |
|---|---|---|---|
| 1. Private core | Local assistant on trusted network | Copy `.env.agent.example` to `.env.agent`, set `SEARXNG_SECRET`, pick installed Ollama model, `docker compose up` | Kiosk opens, `/health` ok |
| 2. Profiles and memory | Separate household memories | Create one consenting profile at a time, save a note | No cross-profile leakage |
| 3. Voice and webcam | Explicit browser media | Grant mic/camera while testing, talk button, optional enrollment image | Visible active state; enrollment only to selected profile |
| 4. Drive import | Document source | Sync Drive folder read-only, import a doc from kiosk | Profile-scoped import, mirror unchanged |
| 5. Action connector | Owned adapter | Deploy narrow connector, set URL/token, minimal allowlists | Proposal visible before delivery; messages/bookings need confirmation |
| 6. Expansion adapters | Vendor APIs/hardware | One adapter at a time | Each reports status, disable control, obeys policy |
```bash
cd agent_server
PYTHONPATH=. python3 -m unittest discover -s tests -v
```
