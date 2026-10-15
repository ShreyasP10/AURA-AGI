# [AUDIT] Comprehensive Codebase Audit: Startup Crashes, Container Health Failures, and Runtime Exceptions
**Labels:** `bug`, `security`, `performance`, `tech-debt`  
**Assignees:** `@ShreyasP10`  
**Milestone:** v1.1.0-patch  
---
## 📌 Summary
A deep static analysis and runtime audit across all 40+ modules (Python, FastAPI, Docker, and frontend JavaScript) identified **20 defects** spanning fatal startup crashes, container health failures, concurrency crashes in the main routing loop, Python 3.13 deprecations, and state synchronization bugs.
---
## 📊 Defect Overview Matrix
| # | File & Location | Severity | Category | Impact |
|---|---|---|---|---|
| 1 | `agent_server/app/main.py:83-85` | 🚨 Critical | Runtime Crash | Fatal `NameError: 'os'` on server startup |
| 2 | `agent_server/Dockerfile:16-17` | 🚨 Critical | Orchestration | Container permanently marked `unhealthy` |
| 3 | `agent_server/app/main.py:138-144` | 🚨 Critical | Authentication | Kiosk UI blocked (403/401) on Docker / LAN |
| 4 | `main.py:494-496` | 🔴 High | Concurrency | ThreadPool future exceptions crash main loop |
| 5 | `main.py:608-614, 666` | 🔴 High | Runtime Crash | `UnboundLocalError: _voice_prompt` in fallback |
| 6 | `ENGINE/STT/whisper_offline.py:69,98` | 🔴 High | Compatibility | `ModuleNotFoundError: 'audioop'` on Python 3.13 |
| 7 | `WEB-3D/app.js:462` & `TOOLS/file_finder.py:56` | 🔴 High | API Integration | Invalid Groq model returns HTTP 400 |
| 8 | `TOOLS/Alpaca_DS_Converser.py:77-79` | 🔴 High | Logic / State | In-memory history loses all user turns |
| 9 | `PLAYGROUND/CAMERA/ocr_live.py:27,50,53` | 🟡 Medium | Resource Leak | Windows `WinError 32` file lock on temp image |
| 10 | `TOOLS/SYSTEM_SETTINGS/app_launcher.py:22` | 🟡 Medium | Logic Bug | `@lru_cache` prevents opening apps more than once |
| 11 | `agent_server/app/services/actions.py:104` | 🟡 Medium | Runtime Crash | `TypeError` comparing naive vs aware datetimes |
| 12 | `agent_server/app/services/agent.py:130-134` | 🟡 Medium | Network / Logic | Web enrichment drops relative redirect URLs |
| 13 | `agent_server/app/services/google_drive.py:48` | 🟡 Medium | Performance | Unbounded `rglob("*")` loads entire mirror to RAM |
| 14 | `BRAIN/AI/VISION/deepInfra_VISION.py:77` | 🟡 Medium | Error Handling | `requests.post` outside `try` crashes caller |
| 15 | `BRAIN/AI/IMAGE/decohere_ai.py:69` | 🟡 Medium | Filesystem | Missing `makedirs` raises `FileNotFoundError` |
| 16 | `TOOLS/AUDIO/Hotword_Detection.py:134-135` | 🟡 Medium | Logic / Index | Custom `.ppn` wake words cause `IndexError` |
| 17 | `TOOLS/RawDog.py:42,68` | 🟢 Low | Security | Autonomous script execution without user prompt |
| 18 | `BRAIN/AI/TEXT/API/openrouter.py:121` | 🟢 Low | Data Integrity | Global `re.sub` corrupts SSE stream tokens |
| 19 | `ENGINE/STT/DevsDoCode.py:320-330` | 🟢 Low | Maintainability | Dead `while True:` loop in `listen()` |
| 20 | `TOOLS/task_board.py:76` & `main.py:442` | 🟢 Low | Defensive Code | Unsafe direct dict indexing causes `KeyError` |
---
## 🔍 Detailed Defect Descriptions & Proposed Fixes
### 🚨 1. Fatal `NameError: name 'os' is not defined` on FastAPI Startup
- **File:** `agent_server/app/main.py:83-85`
- **Severity:** Critical
- **Description:** Lines 83–85 reference `os.environ.get("AURA_DOCS", "0")`, but `os` is never imported in the module. Starting `uvicorn app.main:app` raises an unhandled `NameError` and terminates the process immediately.
- **Fix:**

--- a/agent_server/app/main.py
+++ b/agent_server/app/main.py
@@ -1,6 +1,7 @@
 from __future__ import annotations
 
 import json
+import os
 from contextlib import asynccontextmanager

  

  
🚨 2. Docker Healthcheck Permanently Fails Due to Authenticated /health

  

  
File: agent_server/Dockerfile:16-17, agent_server/app/main.py:110,123

  
Severity: Critical

  
Description: Dockerfile configures HEALTHCHECK with urllib.request.urlopen('http://127.0.0.1:8080/health', timeout=3). Since /health and /healthz both require require_auth, unauthenticated requests return HTTP 401 Unauthorized. Docker marks the container as unhealthy after 3 failed intervals.

  
Fix: Make /healthz a lightweight, unauthenticated liveness probe that only returns {"status": "ok"} without exposing internal database paths or Ollama status:

  

  
diff
--- a/agent_server/app/main.py
+++ b/agent_server/app/main.py
@@ -120,6 +120,6 @@ async def health(request: Request) -> dict:
     }
 
-@app.get("/healthz", include_in_schema=False, dependencies=[Depends(require_auth)])
-async def healthz(request: Request) -> dict:
-    return await health(request)
+@app.get("/healthz", include_in_schema=False)
+async def healthz() -> dict:
+    return {"status": "ok"}

  

  
🚨 3. Kiosk Client Denied Access in Docker & LAN Deployments

  

  
File: agent_server/app/main.py:138-144

  
Severity: Critical

  
Description: /api/client-token restricts requests strictly to peer in ("127.0.0.1", "::1"). In Docker bridge environments (172.x.x.x) or on remote kiosks connecting over LAN (http://192.168.1.20:8080 per KIOSK_DEPLOYMENT.md), the request returns 403 Forbidden. The frontend fails to acquire apiToken, breaking all subsequent API calls (/api/profiles, /api/chat/stream).

  
Fix: Allow private network and loopback IP addresses:

  

  
diff
--- a/agent_server/app/main.py
+++ b/agent_server/app/main.py
@@ -137,8 +137,13 @@ async def client_token(request: Request) -> dict:
-    peer = request.client.host if request.client else ""
-    if peer not in ("127.0.0.1", "::1"):
+    import ipaddress
+    peer = request.client.host if request.client else ""
+    try:
+        client_ip = ipaddress.ip_address(peer)
+        if not (client_ip.is_loopback or client_ip.is_private):
+            raise HTTPException(status_code=403)
+    except ValueError:
         raise HTTPException(status_code=403)

  

  
🔴 4. Unhandled ThreadPool Future Exceptions Crash the Main Loop

  

  
File: main.py:494-496

  
Severity: High

  
Description: f_img.result(), f_cls.result(), and f_def.result() are called directly without try/except. If any parallel DeepInfra call encounters an API timeout, rate limit, or 500 error, calling .result() re-raises the exception and halts the main assistant loop.

  
Fix: Safely resolve futures with a helper:

  

  
diff
--- a/main.py
+++ b/main.py
@@ -493,4 +493,11 @@
-        _img_text = (f_img.result() or "").strip().lower()
-        _cls_res  = (f_cls.result() or "").lower()
-        _def_res  =  f_def.result() or "Sorry, I could not think of a reply."
+        def _safe_res(fut, default=""):
+            try:
+                return fut.result(timeout=0) if fut.done() else default
+            except Exception as e:
+                print(f"[intent future] {e}")
+                return default
+
+        _img_text = (_safe_res(f_img) or "").strip().lower()
+        _cls_res  = (_safe_res(f_cls) or "").lower()
+        _def_res  =  _safe_res(f_def, "Sorry, I could not think of a reply.")

  

  
🔴 5. UnboundLocalError for _voice_prompt on Fallback Cascade

  

  
File: main.py:608-614, 666

  
Severity: High

  
Description: _voice_prompt is assigned on line 609 inside the try: block after calling _lazy_groq.get_client(). If _lazy_groq.get_client() throws an error, execution skips directly to the except: block on line 666, triggering UnboundLocalError: local variable '_voice_prompt' referenced before assignment.

  
Fix: Move _voice_prompt definition above the try: block:

  

  
diff
--- a/main.py
+++ b/main.py
@@ -607,2 +607,6 @@
+        _voice_prompt = (
+            base_prompt + " Reply in 1-2 short sentences for voice. No markdown, no code, no emoji."
+            if _AURA_FAST else base_prompt
+        )
         try:
             _groq = _lazy_groq.get_client()
-            _voice_prompt = ( ... )

  

  
🔴 6. Python 3.13 Crash: audioop Removed from Standard Library

  

  
File: ENGINE/STT/whisper_offline.py:69, 98

  
Severity: High

  
Description: Python 3.13 removed audioop (PEP 594). Invoking listen_vad() on Python 3.13 immediately raises ModuleNotFoundError: No module named 'audioop'.

  
Fix: Provide a pure-Python fallback using struct and math:

  

  
diff
--- a/ENGINE/STT/whisper_offline.py
+++ b/ENGINE/STT/whisper_offline.py
@@ -68,3 +68,14 @@
-        import audioop
+        import struct, math
+        try:
+            import audioop
+        except ModuleNotFoundError:
+            class _AudioOpFallback:
+                @staticmethod
+                def rms(fragment, width):
+                    if not fragment or width != 2:
+                        return 0
+                    count = len(fragment) // 2
+                    shorts = struct.unpack(f"{count}h", fragment)
+                    return int(math.sqrt(sum(s * s for s in shorts) / count)) if count else 0
+            audioop = _AudioOpFallback()

  

  
🔴 7. Invalid Groq Model openai/gpt-oss-20b Fails with HTTP 400

  

  
File: WEB-3D/app.js:462, TOOLS/file_finder.py:56

  
Severity: High

  
Description: Both modules make chat completion calls requesting model openai/gpt-oss-20b, which does not exist on Groq and returns HTTP 400.

  
Fix: Replace with llama-3.1-8b-instant.

  

  

  
🔴 8. In-Memory Conversation History Drops User Utterances

  

  
File: TOOLS/Alpaca_DS_Converser.py:77-79

  
Severity: High

  
Description: update_file(user_query, assistant_response) writes both queries to disk, but only appends assistant_response to self.history. In-memory context degrades into a series of assistant answers without user questions.

  
Fix: Append both the user and assistant turns:

  

  
diff
--- a/TOOLS/Alpaca_DS_Converser.py
+++ b/TOOLS/Alpaca_DS_Converser.py
@@ -77,3 +77,6 @@
         self.store_history(
-            self.history + [{"role": "assistant", "content": assistant_response}]
+            self.history + [
+                {"role": "user", "content": user_query},
+                {"role": "assistant", "content": assistant_response},
+            ]
         )

  

  
🟡 9. Windows File Locking (WinError 32) on Temp OCR Image

  

  
File: PLAYGROUND/CAMERA/ocr_live.py:27, 50, 53

  
Severity: Medium

  
Description: Image.open(image_path) leaves the file handle open on Windows. Subsequent os.remove(path) calls fail with PermissionError: [WinError 32].

  
Fix: Use with Image.open(image_path) as img: return pytesseract.image_to_string(_resize(img.copy())).

  

  

  
🟡 10. @lru_cache on Side-Effecting Process Spawner

  

  
File: TOOLS/SYSTEM_SETTINGS/app_launcher.py:22

  
Severity: Medium

  
Description: Decorating open_app(name: str) with @lru_cache(maxsize=32) prevents launching any application more than once per session, as subsequent calls return the cached response without running subprocess.Popen.

  
Fix: Remove @lru_cache(maxsize=32).

  

  

  
🟡 11. Naive vs. Aware Datetime Comparison TypeError

  

  
File: agent_server/app/services/actions.py:104, 167, agent_server/app/services/executor.py:125

  
Severity: Medium

  
Description: datetime.fromisoformat(value) <= datetime.now(UTC) raises TypeError if value is an offset-naive ISO string.

  
Fix: Attach UTC if dt.tzinfo is None before comparing.

  

  

  
🟡 12. Web Search Enrichment Drops Relative Redirects

  

  
File: agent_server/app/services/agent.py:130-134

  
Severity: Medium

  
Description: On HTTP 301/302 redirects where Location is relative (/path), urlparse(location).hostname is None, causing _is_public_http_url to return False and drop valid sources.

  
Fix: Use urllib.parse.urljoin(url, location) before checking and following redirects.

  

  

  
🟡 13. Unbounded rglob("*") in GoogleDriveMirror

  

  
File: agent_server/app/services/google_drive.py:48

  
Severity: Medium

  
Description: sorted(root.rglob("*"), ...) reads the entire directory tree into memory before filtering extensions, causing high latency and memory spikes on large synced Drives.

  
Fix: Filter file extensions during iteration before sorting.

  

  

  
🟡 14. Unhandled requests.post Exception in deepInfra_VISION.py

  

  
File: BRAIN/AI/VISION/deepInfra_VISION.py:77

  
Severity: Medium

  
Description: Line 77 is placed outside the try block. Network timeouts raise unhandled exceptions in the caller thread.

  
Fix: Move requests.post inside the try block.

  

  

  
🟡 15. Missing os.makedirs Before File Writes

  

  
File: BRAIN/AI/IMAGE/decohere_ai.py:69, TOOLS/SYSTEM_SETTINGS/Alarms.py:65

  
Severity: Medium

  
Description: Writing to ASSETS/image.jpg or ASSETS/alarms.json assumes the directory already exists. In fresh checkouts, this raises FileNotFoundError.

  
Fix: Call os.makedirs(os.path.dirname(path) or ".", exist_ok=True) prior to writing.

  

  

  
🟡 16. Custom Wake Word Index Mismatch in Porcupine

  

  
File: TOOLS/AUDIO/Hotword_Detection.py:134-135

  
Severity: Medium

  
Description: When custom aura*.ppn models are loaded, keyword_index indexes into keyword_paths, but line 135 accesses self.keywords[keyword_index]. This reports the wrong keyword name or raises IndexError.

  
Fix: Check whether custom .ppn models are in use and resolve the keyword from the .ppn file stem.

  

  

  
🟢 17. Autonomous Script Execution Without Prompt

  

  
File: TOOLS/RawDog.py:42, 68

  
Severity: Low / Security

  
Description: _script_confirmation_required = False allows arbitrary code generated by the LLM to run without confirmation.

  
Fix: Default _script_confirmation_required = True.

  

  

  
🟢 18. Global re.sub Corrupts SSE Stream Content

  

  
File: BRAIN/AI/TEXT/API/openrouter.py:121

  
Severity: Low

  
Description: re.sub("data:", "", line) replaces all occurrences of "data:" across the payload rather than just the leading prefix.

  
Fix: Use line.removeprefix("data:").strip().

  

  

  
🟢 19. Redundant while True: Construct in DevsDoCode.py

  

  
File: ENGINE/STT/DevsDoCode.py:320-330

  
Severity: Low

  
Description: while True: returns unconditionally on the first iteration, making the loop construct dead code.

  
Fix: Simplify to a single call without the loop.

  

  

  
🟢 20. Unsafe Dict Access on Tasks

  

  
File: TOOLS/task_board.py:76, main.py:442

  
Severity: Low

  
Description: Direct dictionary indexing (t["text"], t["priority"]) causes KeyError if tasks lack expected keys.

  
Fix: Use .get("text", "") and .get("priority", "none").

  

  

  
✅ Acceptance Criteria & Checklist

  

  
 Fix import os in agent_server/app/main.py

  
 Add unauthenticated /healthz liveness probe for Docker HEALTHCHECK

  
 Permit LAN/Docker bridge client IPs in /api/client-token

  
 Add _safe_res exception guard on parallel futures in main.py

  
 Move _voice_prompt definition above try: block in main.py

  
 Implement audioop pure-Python fallback for Python 3.13 in whisper_offline.py

  
 Replace openai/gpt-oss-20b with llama-3.1-8b-instant in WEB-3D/app.js and file_finder.py

  
 Fix user query persistence in Alpaca_DS_Converser.py

  
 Remove @lru_cache from open_app in app_launcher.py

  
 Normalize naive datetimes to UTC in actions.py and executor.py

  
 Add context manager to Image.open in ocr_live.py

  
 Use urljoin for relative redirect handling in agent.py

  
 Verify test suite passes (pytest test_aura_fixes.py & unittest)
