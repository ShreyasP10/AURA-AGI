import sqlite3
import os
import shutil


def _read_latest_url(history_path: str, copy_name: str, label: str) -> str:
    if not os.path.exists(history_path):
        raise FileNotFoundError(
            f"{label} History not found: {history_path} (Windows only, close browser first if locked)"
        )

    import tempfile
    import uuid

    # Destination path in tempdir to avoid workspace pollution and concurrent file locks
    history_db_path = os.path.join(
        tempfile.gettempdir(), f"{copy_name}_{os.getpid()}_{uuid.uuid4().hex[:8]}.db"
    )

    # Copy the history database to a new location
    try:
        shutil.copy2(history_path, history_db_path)
    except Exception as e:
        raise RuntimeError(f"Cannot copy locked {label} History (close browser): {e}")

    conn = None
    try:
        # Connect to the history database (closed explicitly in finally:
        # sqlite3's context manager only commits, it does NOT close)
        conn = sqlite3.connect(history_db_path)
        cursor = conn.cursor()

        # Execute a query to retrieve the latest URL from the history
        cursor.execute("SELECT url FROM urls ORDER BY last_visit_time DESC LIMIT 1")
        row = cursor.fetchone()
        if not row:
            raise ValueError(f"No URLs in {label} history")

        print("Latest URL:", row[0])
        return row[0]
    finally:
        if conn is not None:
            try:
                conn.close()
            except Exception as e:
                print(f"[error {__file__}] {type(e).__name__}: {e}")
        # Windows holds file locks briefly (SQLite/AV) — retry removal
        import time as _time

        for _attempt in range(5):
            try:
                if os.path.exists(history_db_path):
                    os.remove(history_db_path)
                break
            except Exception as e:
                if _attempt == 4:
                    print(f"[error {__file__}] {type(e).__name__}: {e}")
                else:
                    _time.sleep(0.2)


def get_latest_brave_url() -> str:
    """Latest URL from Brave (default)."""
    brave_history_path = (
        os.path.expanduser("~")
        + r"\AppData\Local\BraveSoftware\Brave-Browser\User Data\Default\History"
    )
    return _read_latest_url(brave_history_path, "BraveHistoryCopy.txt", "Brave")


def get_latest_chrome_url() -> str:
    """Latest URL from Chrome, fallback to Brave if Chrome missing (Brave-first)."""
    chrome_history_path = (
        os.path.expanduser("~")
        + r"\AppData\Local\Google\Chrome\User Data\Default\History"
    )
    if os.path.exists(chrome_history_path):
        try:
            return _read_latest_url(
                chrome_history_path, "ChromeHistoryCopy.txt", "Chrome"
            )
        except Exception as e:
            print(f"Chrome history failed ({e}), trying Brave...")
    return get_latest_brave_url()


# Backwards-compat alias: default browser URL = Brave-first
def get_latest_browser_url() -> str:
    return get_latest_chrome_url()


if __name__ == "__main__":
    latest_url = get_latest_chrome_url()
