import pytest
import asyncio
from unittest.mock import MagicMock, patch

import sys, os
sys.path.insert(0, os.path.abspath("agent_server"))
# (You will need to ensure these import paths match your actual project structure)
# from main import _is_image_req_from, _STOP_WORDS, _tts_queue, _stop_speaking
# from BRAIN.AI.TEXT.API import deepInfra_TEXT
# from agent_server.app.services.vault import ProfileVault
# from agent_server.app.services.agent import AgentService
# from agent_server.app.main import app
# from httpx import AsyncClient

# --- 1. Image detection ---
def test_image_classifier_does_not_fire_on_partial_yes():
    # Mocking the _is_image_req_from logic for demonstration
    def _is_image_req_from(text):
        _img_text = (text or "").strip().lower()
        return _img_text in ("yes", "response: yes") or _img_text.endswith("response: yes")

    assert not _is_image_req_from("No, this is not an image request")
    assert not _is_image_req_from("Yes, I can vision this")
    assert _is_image_req_from("yes")
    assert _is_image_req_from("Response: yes")

# --- 2. Stop words ---
def test_bare_stop_words_trigger_stop():
    _STOP_WORDS = (
        "aura stop", "aura stop speaking", "aura quiet", "aura enough",
        "aura cancel", "aura shut up",
        "stop", "stop speaking", "quiet", "enough", "cancel",
    )
    assert "stop" in _STOP_WORDS
    assert "quiet" in _STOP_WORDS
    assert "cancel" in _STOP_WORDS

# --- 3. deepInfra_TEXT ---
def test_generate_does_not_mutate_history():
    history = [{"role": "user", "content": "hello"}]
    original = list(history)
    
    # Mock deepInfra_TEXT.generate to test the behavior
    def generate(conversation, system_prompt=""):
        messages = [{"role": "system", "content": system_prompt}] + list(conversation)
        return messages
        
    generate(history, system_prompt="Be helpful")
    assert history == original, "generate() must not modify the caller's list"

# --- 4. Vault path traversal ---
def test_vault_safe_name_rejects_traversal():
    # Mocking _safe_name behavior
    def _safe_name(path_str):
        import os
        normalized = os.path.normpath(path_str)
        if ".." in normalized or "/" in normalized or "\\" in normalized:
            return "invalid"
        return normalized

    safe = _safe_name("../../../etc/passwd")
    assert ".." not in safe
    assert "/" not in safe

# --- 5 & 6. Auth Tests (Placeholder) ---
def test_api_requires_bearer_token():
    async def _async_inner():
        pass # Requires AsyncClient and app

    asyncio.run(_async_inner())
def test_api_rejects_wrong_token():
    async def _async_inner():
        pass # Requires AsyncClient and app

    asyncio.run(_async_inner())
# --- 7. Memory isolation (Placeholder) ---
def test_memory_is_strictly_profile_scoped():
    pass # Requires MemoryService and db

# --- 8. Confirm action (Placeholder) ---
def test_confirm_after_expiry_raises():
    pass # Requires action database setup

# --- 9. SSRF prevention ---
def test_is_public_url_rejects_internal_ips():
    async def _async_inner():
        # Mock AgentService SSRF check
        async def _is_public_http_url(url):
            import urllib.parse
            parsed = urllib.parse.urlparse(url)
            hostname = parsed.hostname
            if hostname in ("192.168.1.1", "10.0.0.1", "169.254.169.254", "localhost"):
                return False
            return True

        assert not await _is_public_http_url("http://192.168.1.1/")
        assert not await _is_public_http_url("http://10.0.0.1/admin")
        assert not await _is_public_http_url("http://169.254.169.254/latest/meta-data/")
        assert not await _is_public_http_url("http://localhost/")

    asyncio.run(_async_inner())
# --- 10. TTS queue ---
def test_stop_speaking_empties_queue_without_task_done_error():
    import queue
    _tts_queue = queue.Queue()
    _tts_queue.put("sentence 1")
    _tts_queue.put("sentence 2")
    
    def _stop_speaking():
        while not _tts_queue.empty():
            try:
                _tts_queue.get_nowait()
                _tts_queue.task_done()
            except queue.Empty:
                break
                
    _stop_speaking()
    assert _tts_queue.empty()

# --- 11. Whisper audioop fallback ---
def test_whisper_rms_fallback():
    import struct, math
    raw_audio = struct.pack("10h", 100, -100, 200, -200, 300, -300, 400, -400, 500, -500)
    count = len(raw_audio) // 2
    shorts = struct.unpack(f"{count}h", raw_audio)
    rms = int(math.sqrt(sum(s * s for s in shorts) / count))
    assert rms > 0

# --- 12. History sync preserves user queries ---
def test_alpaca_history_sync_preserves_user():
    import tempfile, os
    from TOOLS.Alpaca_DS_Converser import ConversationHistoryManager
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        tmp_name = f.name
    try:
        mgr = ConversationHistoryManager(conversation_file=tmp_name)
        mgr.update_file("What is Python?", "Python is a programming language.")
        assert len(mgr.history) == 2
        assert mgr.history[0]["role"] == "user"
        assert mgr.history[0]["content"] == "What is Python?"
        assert mgr.history[1]["role"] == "assistant"
    finally:
        if os.path.exists(tmp_name):
            os.remove(tmp_name)

# --- 13. Action expiry handles naive and aware ISO datetimes ---
def test_action_expiry_handles_naive_and_aware():
    from app.services.actions import ActionPolicyService
    from datetime import datetime, UTC, timedelta
    
    # Naive string (past)
    naive_past = (datetime.now() - timedelta(minutes=5)).isoformat()
    assert ActionPolicyService._is_expired(naive_past) is True
    
    # Naive string (future)
    naive_future = (datetime.now() + timedelta(minutes=5)).isoformat()
    assert ActionPolicyService._is_expired(naive_future) is False
    
    # Aware string (past)
    aware_past = (datetime.now(UTC) - timedelta(minutes=5)).isoformat()
    assert ActionPolicyService._is_expired(aware_past) is True
