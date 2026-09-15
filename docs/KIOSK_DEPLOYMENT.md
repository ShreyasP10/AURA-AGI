# Galaxy Book Kiosk Deployment
The Galaxy Book is a **thin kiosk client**, not the assistant server.
> **Do not install Ollama, Docker, a Google Drive mirror, or a local vector database on the Galaxy Book.**
## Operating-system choices
| Client path | When to use it | Included launcher |
|---|---|---|
| Lightweight Linux desktop | Dedicated single-purpose kiosk | `deployment/kiosk/linux/aura-kiosk.sh` |
| Existing Windows installation | Touchscreen/LTE/camera already work | `deployment/kiosk/windows/start-aura-kiosk.cmd` |
## Server address
Give the Docker server a stable address, e.g. `http://192.168.1.20:8080`.
## Linux profile
```bash
chmod +x ~/aura-kiosk.sh
AURA_AGENT_URL=http://192.168.1.20:8080 ~/aura-kiosk.sh
```
## Windows profile
Set `AURA_AGENT_URL` in the `.cmd`, double-click to verify, then Startup folder shortcut for autostart.
