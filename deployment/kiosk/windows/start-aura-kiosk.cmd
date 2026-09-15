@echo off
setlocal
REM Configure the agent address once, or override it before calling this script.
REM AURA_AGENT_URL is current; JARVIS_AGENT_URL kept as fallback.
if "%AURA_AGENT_URL%"=="" if not "%JARVIS_AGENT_URL%"=="" set "AURA_AGENT_URL=%JARVIS_AGENT_URL%"
if "%AURA_AGENT_URL%"=="" set "AURA_AGENT_URL=http://127.0.0.1:8080"
set "EDGE=%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe"
if not exist "%EDGE%" set "EDGE=%ProgramFiles%\Microsoft\Edge\Application\msedge.exe"
if not exist "%EDGE%" (
  echo Microsoft Edge was not found. Install Edge or edit this script to point to Chrome.
  exit /b 1
)
start "AURA Kiosk" "%EDGE%" --kiosk "%AURA_AGENT_URL%" --edge-kiosk-type=fullscreen --no-first-run
endlocal
