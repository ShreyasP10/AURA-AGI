from __future__ import annotations

from pathlib import Path

import yaml

repo_root = Path(__file__).resolve().parents[2]
compose_path = repo_root / "compose.yml"
document = yaml.safe_load(compose_path.read_text(encoding="utf-8"))
assert document["name"] == "aura-kiosk-agent"
services = document["services"]
assert {"agent-server", "searxng"}.issubset(services)
agent = services["agent-server"]
assert "searxng" in agent["depends_on"]
assert any("agent_data:/data" in volume for volume in agent["volumes"])
assert "GOOGLE_DRIVE_SYNC_DIR" in agent["environment"]
assert agent["read_only"] is True
assert "no-new-privileges:true" in agent["security_opt"]
print("Compose YAML structure validated.")
