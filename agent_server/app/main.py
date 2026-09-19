from __future__ import annotations

import json
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncIterator

from fastapi import FastAPI, HTTPException, Request, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import secrets
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

from app.adapters.ollama import OllamaClient
from app.adapters.searxng import SearxngClient
from app.config import get_settings
from app.db import Database
from app.models import (
    ActionConfirmation,
    ActionProposalRequest,
    ActionResponse,
    ActionRuleCreate,
    ChatRequest,
    DriveImportRequest,
    EnrollmentImageRequest,
    MediaCaptureRequest,
    MemoryCreate,
    ProfileCreate,
    ProfileResponse,
    SkillStateUpdate,
    TaskPlanRequest,
    VaultSaveRequest,
)
from app.services.actions import ActionPolicyService
from app.services.agent import AgentService
from app.services.executor import ActionExecutor
from app.services.google_drive import GoogleDriveMirror
from app.services.memory import MemoryService
from app.services.skills import SkillRegistry
from app.services.tasks import TaskPlanner
from app.services.vault import ProfileVault

settings = get_settings()
static_dir = Path(__file__).parent / "static"

_bearer = HTTPBearer(auto_error=False)
def require_auth(creds: HTTPAuthorizationCredentials | None = Security(_bearer)) -> None:
    if not settings.api_secret:
        return
    if not creds or not secrets.compare_digest(creds.credentials, settings.api_secret):
        raise HTTPException(status_code=401, detail="Unauthorized")



@asynccontextmanager
async def lifespan(app: FastAPI):
    database = Database(settings.database_path)
    database.initialize(settings.owner_profile_name)
    memory = MemoryService(database, settings.max_context_chars)
    app.state.database = database
    app.state.ollama = OllamaClient(settings)
    app.state.searxng = SearxngClient(settings)
    app.state.memory = memory
    app.state.agent = AgentService(
        settings, database, app.state.ollama, app.state.searxng, memory
    )
    app.state.actions = ActionPolicyService(database)
    app.state.executor = ActionExecutor(settings, database)
    app.state.tasks = TaskPlanner(database, app.state.ollama, app.state.actions)
    app.state.skills = SkillRegistry(database)
    app.state.skills.initialize()
    app.state.vault = ProfileVault(settings)
    app.state.google_drive = GoogleDriveMirror(settings, database, app.state.vault)
    yield


app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)

if settings.public_origin:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            item.strip() for item in settings.public_origin.split(",") if item.strip()
        ],
        allow_credentials=False,
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type"],
    )

app.mount("/static", StaticFiles(directory=static_dir), name="static")


def database(request: Request) -> Database:
    return request.app.state.database


def actions(request: Request) -> ActionPolicyService:
    return request.app.state.actions


@app.get("/health")
async def health(request: Request) -> dict:
    ollama = await request.app.state.ollama.health()
    search = await request.app.state.searxng.health()
    return {
        "status": "ok" if ollama.get("reachable") else "degraded",
        "service": settings.app_name,
        "ollama": ollama,
        "search": search,
        "database": str(settings.database_path),
    }


@app.get("/healthz", include_in_schema=False)
async def healthz(request: Request) -> dict:
    return await health(request)


from fastapi.responses import Response
@app.get("/favicon.ico", include_in_schema=False)
def favicon() -> Response:
    svg = b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><circle cx="16" cy="16" r="14" fill="#07111f" stroke="#48c6ff" stroke-width="2"/><text x="16" y="22" text-anchor="middle" fill="#48c6ff" font-size="16" font-family="sans-serif">J</text></svg>'
    return Response(content=svg, media_type="image/svg+xml", headers={"Cache-Control": "public, max-age=86400"})


@app.get("/api/client-token", include_in_schema=False)
async def client_token(request: Request) -> dict:
    host = request.headers.get("host", "")
    if not host.startswith("127.") and not host.startswith("localhost"):
        raise HTTPException(status_code=403)
    return {"token": settings.api_secret}

@app.get("/api/profiles", response_model=list[ProfileResponse], dependencies=[Depends(require_auth)])
def list_profiles(request: Request) -> list[dict]:
    return database(request).list_profiles()


@app.post("/api/profiles", response_model=ProfileResponse, status_code=201, dependencies=[Depends(require_auth)])
def create_profile(payload: ProfileCreate, request: Request) -> dict:
    try:
        profile = database(request).create_profile(
            payload.profile_id,
            payload.display_name,
            payload.consented,
            payload.preferences,
        )
        database(request).audit(
            "profile_created",
            {"display_name": payload.display_name},
            payload.profile_id,
        )
        return profile
    except Exception as error:
        raise HTTPException(
            status_code=409, detail=f"Could not create profile: {error}"
        ) from error


@app.get("/api/conversations/{profile_id}", dependencies=[Depends(require_auth)])
def recent_conversation(profile_id: str, request: Request) -> dict:
    if not database(request).get_profile(profile_id):
        raise HTTPException(status_code=404, detail="Profile not found.")
    return {
        "profile_id": profile_id,
        "turns": database(request).recent_turns(profile_id, limit=40),
    }


@app.get("/api/skills", dependencies=[Depends(require_auth)])
def list_skills(request: Request) -> dict:
    return {"skills": request.app.state.skills.list()}


@app.post("/api/skills/{skill_id}", dependencies=[Depends(require_auth)])
def set_skill_state(skill_id: str, payload: SkillStateUpdate, request: Request) -> dict:
    skill = request.app.state.skills.set_enabled(skill_id, payload.enabled)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found.")
    return skill


@app.post("/api/memories", status_code=201, dependencies=[Depends(require_auth)])
def create_memory(payload: MemoryCreate, request: Request) -> dict:
    if not database(request).get_profile(payload.profile_id):
        raise HTTPException(status_code=404, detail="Profile not found.")
    memory = request.app.state.memory.remember(
        payload.profile_id, payload.content, payload.category, payload.importance
    )
    database(request).audit(
        "memory_saved",
        {"memory_id": memory["memory_id"], "category": payload.category},
        payload.profile_id,
    )
    return memory


@app.post("/api/vault", status_code=201, dependencies=[Depends(require_auth)])
def save_to_vault(payload: VaultSaveRequest, request: Request) -> dict:
    if not database(request).get_profile(payload.profile_id):
        raise HTTPException(status_code=404, detail="Profile not found.")
    record = request.app.state.vault.save_text(
        payload.profile_id, payload.title, payload.content, payload.category
    )
    database(request).audit("vault_item_saved", record, payload.profile_id)
    return record


@app.get("/api/vault/{profile_id}", dependencies=[Depends(require_auth)])
def list_vault(profile_id: str, request: Request) -> dict:
    if not database(request).get_profile(profile_id):
        raise HTTPException(status_code=404, detail="Profile not found.")
    return {
        "profile_id": profile_id,
        "files": request.app.state.vault.list_files(profile_id),
    }


@app.get("/api/google-drive", dependencies=[Depends(require_auth)])
def google_drive_status(request: Request) -> dict:
    return request.app.state.google_drive.status()


@app.get("/api/google-drive/files", dependencies=[Depends(require_auth)])
def list_google_drive_files(request: Request) -> dict:
    drive = request.app.state.google_drive
    return {"status": drive.status(), "files": drive.list_files()}


@app.post("/api/google-drive/import", status_code=201, dependencies=[Depends(require_auth)])
def import_google_drive_file(payload: DriveImportRequest, request: Request) -> dict:
    try:
        return request.app.state.google_drive.import_file(
            payload.profile_id, payload.relative_path, payload.remember_excerpt
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/chat/stream", dependencies=[Depends(require_auth)])
async def chat_stream(payload: ChatRequest, request: Request) -> StreamingResponse:
    async def events() -> AsyncIterator[str]:
        async for event in request.app.state.agent.stream_chat(
            payload.profile_id, payload.message, payload.include_web
        ):
            yield json.dumps(event, ensure_ascii=False) + "\n"

    return StreamingResponse(
        events(),
        media_type="application/x-ndjson",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.post("/api/tasks/plan", dependencies=[Depends(require_auth)])
async def plan_task(payload: TaskPlanRequest, request: Request) -> dict:
    try:
        return await request.app.state.tasks.plan(payload.profile_id, payload.request)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/action-rules", status_code=201, dependencies=[Depends(require_auth)])
def create_action_rule(payload: ActionRuleCreate, request: Request) -> dict:
    try:
        return actions(request).create_rule(
            payload.rule_id,
            payload.profile_id,
            payload.action_type,
            payload.display_name,
            payload.allowed_targets,
            payload.expires_at,
            payload.enabled,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/actions/propose", response_model=ActionResponse, status_code=201, dependencies=[Depends(require_auth)])
def propose_action(payload: ActionProposalRequest, request: Request) -> dict:
    try:
        return actions(request).propose(
            payload.profile_id,
            payload.action_type,
            payload.summary,
            payload.payload,
            payload.rule_id,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/actions/{action_id}/confirm", response_model=ActionResponse, dependencies=[Depends(require_auth)])
def confirm_action(
    action_id: str, payload: ActionConfirmation, request: Request
) -> dict:
    try:
        return actions(request).confirm(action_id, payload.confirmation_phrase)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/actions/{action_id}/execute", dependencies=[Depends(require_auth)])
async def execute_action(action_id: str, request: Request) -> dict:
    try:
        return await request.app.state.executor.execute(action_id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/api/profiles/{profile_id}/enrollment-image", status_code=201, dependencies=[Depends(require_auth)])
def save_enrollment_image(
    profile_id: str, payload: EnrollmentImageRequest, request: Request
) -> dict:
    profile = database(request).get_profile(profile_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found.")
    if not profile["consented"] or not payload.consented:
        raise HTTPException(
            status_code=400,
            detail="A consenting profile and explicit capture consent are required.",
        )
    try:
        record = request.app.state.vault.save_enrollment_image(
            profile_id, payload.image_data_url, payload.label
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    database(request).audit("profile_enrollment_image_saved", record, profile_id)
    return {
        **record,
        "message": "Enrollment image stored locally for this consenting profile. No recognition or background matching was performed.",
    }


@app.post("/api/media/capture", status_code=202, dependencies=[Depends(require_auth)])
def record_media_capture(payload: MediaCaptureRequest, request: Request) -> dict:
    if not payload.consented:
        raise HTTPException(
            status_code=400,
            detail="Explicit browser consent is required before media input is recorded.",
        )
    if not database(request).get_profile(payload.profile_id):
        raise HTTPException(status_code=404, detail="Profile not found.")
    database(request).audit(
        "media_capture_authorized",
        {"kind": payload.kind, "label": payload.label},
        payload.profile_id,
    )
    return {
        "accepted": True,
        "message": "Media permission state was recorded. Raw media upload is disabled until a dedicated opt-in adapter is configured.",
    }


@app.get("/", include_in_schema=False)
def kiosk() -> FileResponse:
    return FileResponse(static_dir / "index.html")
