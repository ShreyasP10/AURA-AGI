"""
Author: AURA Team (Shreyas)
Project: Realtime Speech to Text Listener
Description: A Python script that uses Selenium to interact with a website and listen to user input & print them in real time.
"""

from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
# import os


class SpeechToTextListener:
    """A class for performing speech-to-text using a web-based service."""

    def __init__(
        self,
        website_path: str = None,  # auto-detect local file with 2s silence fix
        language: str = "hi-IN",
        wait_time: int = 30,  # longer for slow mic start (was 10, cut long speech)
        silence_timeout: int = None,  # ms, from AURA_SILENCE_MS or 3000
        browser: str = None,  # "brave" or "chrome" (default from AURA_BROWSER env or brave)
        brave_path: str = None,
    ):  # explicit brave.exe path
        import os

        if silence_timeout is None:
            try:
                silence_timeout = int(os.environ.get("AURA_SILENCE_MS", "3000"))
            except Exception:
                silence_timeout = 3000
        silence_timeout = max(800, min(8000, silence_timeout))
        self.silence_timeout = silence_timeout
        if website_path is None:
            # use local src/index.html with silence via ?silence= (continuous=true)
            local_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "src", "index.html"
            )
            website_path = "file:///" + local_path.replace("\\", "/") + f"?silence={silence_timeout}"
        elif "?silence=" not in website_path and "index.html" in website_path:
            website_path = website_path + f"?silence={silence_timeout}"
        if browser is None:
            browser = os.environ.get("AURA_BROWSER", "brave").lower()

        """Initializes the STT class with the given website path and language."""
        self.website_path = website_path
        self.language = language
        self.browser = browser
        self.chrome_options = Options()
        self.chrome_options.add_argument("--use-fake-ui-for-media-stream")
        self.chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        )
        # AURA_HEADLESS=0 runs headed for mic debugging (headless has no real mic)
        _headless = os.environ.get("AURA_HEADLESS", "1") != "0"
        if _headless:
            self.chrome_options.add_argument("--headless=new")
        else:
            print("STT headed mode (AURA_HEADLESS=0) — browser window will open")
        # file:// mic access
        self.chrome_options.add_argument("--allow-file-access-from-files")
        self.chrome_options.add_argument("--disable-features=DialMediaRouteProvider")
        # Isolated profile so running Brave/Chrome doesn't lock Default (fixes NoSuchWindow target closed)
        import tempfile

        _profile = os.path.join(tempfile.gettempdir(), f"aura-{browser}-profile")
        try:
            os.makedirs(_profile, exist_ok=True)
        except Exception:
            pass
        self.chrome_options.add_argument(f"--user-data-dir={_profile}")
        self.chrome_options.add_argument("--no-default-browser-check")
        self.chrome_options.add_argument("--no-first-run")
        # Stability flags: fix SessionNotCreated (version/origin) + headless crashes
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("--remote-allow-origins=*")
        self.chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-automation"]
        )
        if browser == "brave":
            # Brave Shields blocks Google Web Speech (network) — disable shields features
            # Brave is Chromium-based, reuse ChromeDriver with brave binary
            self.chrome_options.add_argument(
                "--disable-features=BraveShields,BraveAdblock"
            )
            candidates = [
                brave_path,
                os.environ.get("BRAVE_PATH"),
                r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
                r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
                os.path.expandvars(
                    r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\Application\brave.exe"
                ),
            ]
            found = next((p for p in candidates if p and os.path.exists(p)), None)
            if not found:
                raise FileNotFoundError(
                    "Brave not found. Set BRAVE_PATH env or pass brave_path. Searched: "
                    + ", ".join([str(c) for c in candidates if c])
                )
            self.chrome_options.binary_location = found
            print(f"Using Brave: {found}")
        try:
            self.driver = webdriver.Chrome(options=self.chrome_options)
        except Exception as e:
            # Surface full cause: version mismatch is the usual suspect
            print(f"\nSTT browser failed to start ({type(e).__name__}): {str(e)[:500]}")
            if browser == "brave":
                # Auto-fallback: Brave driver mismatch -> try Chrome same profile flags
                print("Trying Chrome fallback...")
                try:
                    from selenium.webdriver.chrome.options import Options as _Opts
                    _co = _Opts()
                    _co.add_argument("--use-fake-ui-for-media-stream")
                    _co.add_argument("--allow-file-access-from-files")
                    _co.add_argument("--no-sandbox")
                    _co.add_argument("--disable-dev-shm-usage")
                    _co.add_argument("--remote-allow-origins=*")
                    _co.add_argument(f"--user-data-dir={_profile}-chrome")
                    _co.add_argument("--no-default-browser-check")
                    _co.add_argument("--no-first-run")
                    if os.environ.get("AURA_HEADLESS", "1") != "0":
                        _co.add_argument("--headless=new")
                    self.chrome_options = _co
                    self.browser = "chrome"
                    self.driver = webdriver.Chrome(options=self.chrome_options)
                    print("Chrome fallback started.")
                except Exception as e2:
                    print(f"Chrome fallback also failed ({type(e2).__name__}): {str(e2)[:300]}")
                    print("Fix: update browser + `pip install -U selenium`, or use AURA_TEXT_MODE=1.")
                    raise
            else:
                print("Fix: update browser + `pip install -U selenium`, or use AURA_TEXT_MODE=1.")
                raise
        self.wait = WebDriverWait(self.driver, wait_time)
        try:
            print("Made By \u2764\ufe0f @AURA-Team")
        except UnicodeEncodeError:
            print("Made By @AURA-Team")

    def stream(self, content: str):
        """Prints the given content to the console with a yellow color, overwriting previous output, with "speaking..." added."""
        print("\033[96m\rUser Speaking: \033[93m" + f" {content}", end="", flush=True)

    def get_text(self) -> str:
        """Retrieves the transcribed text from the website."""
        return self.driver.find_element(By.ID, "convert_text").text

    def select_language(self):
        """Selects the language from the dropdown using JavaScript."""
        self.driver.execute_script(
            f"""
            var select = document.getElementById('language_select');
            select.value = '{self.language}';
            var event = new Event('change');
            select.dispatchEvent(event);
            """
        )

    def verify_language_selection(self):
        """Verifies if the language is correctly selected."""
        language_select = self.driver.find_element(By.ID, "language_select")
        selected_language = language_select.find_element(
            By.CSS_SELECTOR, "option:checked"
        ).get_attribute("value")
        return selected_language == self.language

    def main(self, timeout_s: int = 45) -> Optional[str]:
        """Performs speech-to-text conversion and returns the transcribed text."""
        import time as _t
        try:
            self.driver.get(self.website_path)
        except Exception as e:
            # driver died (Brave crash / ConnectionReset) -> recreate once
            print(f"\nSTT driver error ({e}), restarting browser...")
            try:
                self.restart()
            except Exception as e2:
                print(f"STT restart failed: {e2}")
                return None
            try:
                self.driver.get(self.website_path)
            except Exception as e3:
                print(f"STT still failing: {e3}")
                return None

        # Ensure the dropdown options are fully loaded before selecting
        try:
            self.wait.until(EC.presence_of_element_located((By.ID, "language_select")))
        except Exception as e:
            print(f"\nSTT page load timeout: {e}")
            return None
        
        # Select the language using JavaScript
        try:
            self.select_language()
        except Exception:
            pass

        # Verify the language selection (non-fatal)
        try:
            if not self.verify_language_selection():
                print("\nSTT warn: language select failed, continuing anyway")
        except Exception:
            pass

        try:
            self.driver.find_element(By.ID, "click_to_record").click()
        except Exception as e:
            print(f"\nSTT record click failed: {e}")
            return None

        try:
            is_recording = self.wait.until(
                EC.presence_of_element_located((By.ID, "is_recording"))
            )
        except Exception as e:
            print(f"\nSTT recording flag timeout: {e}")
            return None

        print("\033[94m\rListening... (speak now, or Ctrl+C for typing)\033[0m", end="", flush=True)
        start = _t.time()
        last_text = ""
        while True:
            _t.sleep(0.25)  # was tight loop hammering chromedriver -> ConnectionReset
            if _t.time() - start > timeout_s:
                print(f"\nSTT timeout after {timeout_s}s, use typing.")
                try:
                    return self.get_text() or None
                except Exception:
                    return None
            try:
                is_recording = self.driver.find_element(By.ID, "is_recording")
            except Exception as e:
                print(f"\nSTT browser closed ({type(e).__name__}), use typing.")
                return None
            if not is_recording.text.startswith("Recording: True"):
                break
            try:
                text = self.get_text()
            except Exception:
                break
            if text and text != last_text:
                self.stream(text)
                last_text = text

        try:
            return self.get_text()
        except Exception:
            return last_text or None

    def restart(self):
        """Quit and recreate the webdriver (Brave crash recovery)."""
        try:
            self.driver.quit()
        except Exception:
            pass
        import time as _t
        _t.sleep(1.0)
        from selenium import webdriver as _wd
        self.driver = _wd.Chrome(options=self.chrome_options)
        from selenium.webdriver.support.ui import WebDriverWait as _W
        self.wait = _W(self.driver, 30)

    def listen(self, prints: bool = False, timeout_s: int = 45) -> Optional[str]:
        """Starts the listening process by navigating to the website, selecting the desired language, and
        initiating speech-to-text conversion. The function returns the transcribed text if the
        listening process completes successfully.
        """
        import time as _t
        deadline = _t.time() + timeout_s + 15
        while True:
            if _t.time() > deadline:
                return None
            result = self.main(timeout_s=timeout_s)
            if result and len(result.strip()) != 0:
                print("\r" + " " * (len(result) + 16) + "\r", end="", flush=True)
                if prints:
                    print("\033[92m\rYOU SAID: " + f"{result}\033[0m\n")
                return result
            # None/empty = timeout or fail -> return None so caller falls back to typing
            return result


if __name__ == "__main__":
    listener = SpeechToTextListener(
        language="hi-IN"
    )  # You can specify the desired language here
    speech = listener.listen()
    print("FINAL EXTRACTION: ", speech)
