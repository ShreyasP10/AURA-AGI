# Deployment Security and Privacy Controls
| Component | Network exposure | Container controls | Persistent data |
|---|---|---|---|
| `agent-server` | Only published service; bind to trusted LAN/loopback | Non-root `app`, read-only rootfs, `/tmp` 64m, dropped caps, `no-new-privileges`, PID 256 | `agent_data` volume: SQLite, vault, enrollment images |
| `searxng` | Internal Compose network only | Same hardening, no published port | Settings + cache volumes |
| Google Drive mirror | Never a service | Read-only mount | Explicit profile-scoped import |
Enrollment storage is not facial recognition. No background matching, identification, continuous recording, or remote ingestion.
Before household use: strong `SEARXNG_SECRET`, installed Ollama model, restricted port, `.env.agent` out of git.
