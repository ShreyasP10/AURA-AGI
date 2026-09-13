import sqlite3
import os
import shutil

def get_latest_chrome_url() -> str:
    """
    Retrieves the URL of the most recent webpage visited in Google Chrome.

    Returns:
        str: The URL of the most recent webpage visited in Google Chrome.
    """
    chrome_history_path = os.path.expanduser('~') + r"\AppData\Local\Google\Chrome\User Data\Default\History"
    if not os.path.exists(chrome_history_path):
        raise FileNotFoundError(f"Chrome History not found: {chrome_history_path} (Windows Chrome only, close Chrome first if locked)")
    
    # Destination path for the copy of the history file
    history_db_path = os.path.join(os.getcwd(), "ChromeHistoryCopy.txt")

    # Copy the Chrome history database to a new location
    try:
        shutil.copy2(chrome_history_path, history_db_path)
    except Exception as e:
        raise RuntimeError(f"Cannot copy locked Chrome History (close Chrome): {e}")

    try:
        # Connect to the Chrome history database
        conn = sqlite3.connect(history_db_path)
        cursor = conn.cursor()

        # Execute a query to retrieve the latest URL from the history
        cursor.execute("SELECT url FROM urls ORDER BY last_visit_time DESC LIMIT 1")
        row = cursor.fetchone()
        if not row:
            raise ValueError("No URLs in Chrome history")

        # Close the connection
        conn.close()

        print("Latest URL:", row[0])
        return row[0]
    finally:
        try:
            if os.path.exists(history_db_path):
                os.remove(history_db_path)
        except Exception:
            pass

if __name__ == "__main__":
    latest_url = get_latest_chrome_url()
