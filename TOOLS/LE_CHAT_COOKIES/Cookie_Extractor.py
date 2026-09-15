from selenium import webdriver
import posixpath
import os
from typing import Optional, Dict

# print(os.path.join(os.getcwd(), "ASSETS/USERDATA/LE CHAT").replace(os.sep, '/'))
# print(posixpath.normpath(os.path.join(os.getcwd(), "ASSETS/USERDATA/LE CHAT").replace(os.sep, '/')))


def get_ory_session_cookie(
    profile_path: str = posixpath.normpath(
        os.path.join(os.getcwd(), "ASSETS/USERDATA/LE CHAT").replace(os.sep, "/")
    ),
    verbose: bool = True,
    browser: str = None,  # "brave" default, or "chrome"
) -> Optional[Dict[str, str]]:
    """
    Opens a Brave (default) / Chrome webdriver with the specified profile and retrieves the 'ory_session_coolcurranf83m3srkfl' cookie.

    Args:
        profile_path (str): The path to the browser profile directory.
        verbose (bool): Whether to print verbose output during execution. Defaults to True.
        browser (str): "brave" or "chrome". Default from AURA_BROWSER env or brave.

    Returns:
        Optional[Dict[str, str]]: The 'ory_session_coolcurranf83m3srkfl' cookie as a dictionary, or None if not found.
    """
    if browser is None:
        browser = os.environ.get("AURA_BROWSER", "brave").lower()
    if verbose:
        print(
            f"\033[94mInitializing {browser} webdriver with profile: {profile_path}\033[0m"
        )

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_path}")
    options.add_argument("--profile-directory=Default")
    options.add_argument("--headless")
    if browser == "brave":
        candidates = [
            os.environ.get("BRAVE_PATH"),
            r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
            r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe",
            os.path.expandvars(r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\Application\brave.exe"),
        ]
        found = next((p for p in candidates if p and os.path.exists(p)), None)
        if found:
            options.binary_location = found
            if verbose:
                print(f"\033[94mUsing Brave: {found}\033[0m")

    driver = webdriver.Chrome(options=options)
    if verbose:
        print("\033[94mNavigating to https://chat.mistral.ai/\033[0m")

    driver.get("https://chat.mistral.ai/")

    if verbose:
        print("\033[94mRetrieving cookies...\033[0m")

    cookies = driver.get_cookies()
    driver.quit()

    for cookie in cookies:
        if verbose:
            print(f"\033[94mChecking cookie: {cookie['name']}\033[0m")
        if cookie["name"] == "ory_session_coolcurranf83m3srkfl":
            if verbose:
                print(
                    f"\033[92mFound 'ory_session_coolcurranf83m3srkfl' cookie:\033[0m\n\033[93m{cookie}\033[0m"
                )
            if verbose:
                print("\033[94mCookie found successfully!\033[0m")
            return cookie

    if verbose:
        print("\033[94mCookie 'ory_session_coolcurranf83m3srkfl' not found.\033[0m")

    return None


if __name__ == "__main__":
    ory_session_cookie = get_ory_session_cookie()
