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
        wait_time: int = 10,
        silence_timeout: int = 2000,  # ms, for continuous listening
        browser: str = None,  # "chrome" or "brave" (default from AURA_BROWSER env or chrome)
        brave_path: str = None,
    ):  # explicit brave.exe path
        import os

        if website_path is None:
            # use local src/index.html with 2s silence fix (continuous=true)
            local_path = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "src", "index.html"
            )
            website_path = "file:///" + local_path.replace("\\", "/")
        if browser is None:
            browser = os.environ.get("AURA_BROWSER", "chrome").lower()

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
        self.driver = webdriver.Chrome(options=self.chrome_options)
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

    def main(self) -> Optional[str]:
        """Performs speech-to-text conversion and returns the transcribed text."""
        self.driver.get(self.website_path)

        # Ensure the dropdown options are fully loaded before selecting
        self.wait.until(EC.presence_of_element_located((By.ID, "language_select")))

        # Select the language using JavaScript
        self.select_language()

        # Verify the language selection
        if not self.verify_language_selection():
            print(
                f"Error: Failed to select the correct language. Selected: {self.verify_language_selection():}, Expected: {self.language}"
            )
            return None

        self.driver.find_element(By.ID, "click_to_record").click()

        is_recording = self.wait.until(
            EC.presence_of_element_located((By.ID, "is_recording"))
        )

        print("\033[94m\rListening...", end="", flush=True)
        while is_recording.text.startswith("Recording: True"):
            text = self.get_text()
            if text:
                self.stream(text)
            is_recording = self.driver.find_element(By.ID, "is_recording")

        return self.get_text()

    def listen(self, prints: bool = False) -> Optional[str]:
        """Starts the listening process by navigating to the website, selecting the desired language, and
        initiating speech-to-text conversion. The function returns the transcribed text if the
        listening process completes successfully.
        """
        while True:
            result = self.main()
            if result and len(result) != 0:
                print("\r" + " " * (len(result) + 16) + "\r", end="", flush=True)
                if prints:
                    print("\033[92m\rYOU SAID: " + f"{result}\033[0m\n")
                break
        return result


if __name__ == "__main__":
    listener = SpeechToTextListener(
        language="hi-IN"
    )  # You can specify the desired language here
    speech = listener.listen()
    print("FINAL EXTRACTION: ", speech)
