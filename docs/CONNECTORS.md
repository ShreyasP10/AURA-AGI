# Connector and Google Drive Setup
The agent server does **not** contain account passwords, browser cookies, Google OAuth client secrets, or smart-device credentials. It creates a reviewable action proposal, enforces its confirmation or trusted-rule policy, and only then calls a connector that the owner configures.
## Action connector contract
Set `ACTION_WEBHOOK_URL` to a service you own. The agent sends a JSON `POST` only after an action reaches an executable state.
```json
{
  "action_id": "opaque action identifier",
  "profile_id": "owner",
  "action_type": "message | booking | file_transfer | location_share | device_control",
  "summary": "human-readable description",
  "payload": {},
  "rule_id": "optional trusted-rule identifier"
}
```
If configured, `ACTION_WEBHOOK_TOKEN` is delivered as a bearer token.
| Action type | Default approval path | Connector expectation |
|---|---|---|
| Message or booking | Kiosk typed or voice confirmation, then a separate delivery tap | Draft/send or reservation adapter owned by the household |
| File transfer | Named target must match an enabled owner-managed rule | Local share, USB, Bluetooth, or other allowlisted transfer adapter |
| Location share | Named recipient must match an enabled owner-managed rule | Family-location provider adapter with explicit recipient restriction |
| Device control | Named device must match an enabled owner-managed rule | Smart-home bridge constrained to configured device IDs |
## Google Drive mirror
1. Create a dedicated folder such as `AURA/Import`.
2. Sync or mount that folder on the Docker host (Drive desktop client or `rclone` mount).
3. Mount read-only into the container and set `GOOGLE_DRIVE_SYNC_DIR` to its container path.
4. From the kiosk, explicitly import a supported text document (`.txt/.md/.csv/.json/.log`, 2 MB max) into a profile vault.
