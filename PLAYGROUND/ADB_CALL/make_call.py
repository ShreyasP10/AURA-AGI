import subprocess


def call(number: str = "7272733232", isd_code: str = "+91") -> str:
    """
    Initiates a phone call to the specified number using the ADB command.

    Parameters:
    - number (str): The phone number to call. Defaults to your NUMBER
    - isd_code (str): The ISD (International Subscriber Dialing) code. Defaults to "+91".

    Returns:
    - str: A message indicating the status of the call initiation process.
    """

    import re as _re

    # Validate: digits only (plus optional leading + on ISD) — never pass raw
    # voice input to a shell.
    number = _re.sub(r"\D", "", number or "")
    isd_code = "+" + _re.sub(r"\D", "", isd_code or "")
    if not number:
        return "No phone number provided."
    command = [
        "adb.exe",
        "shell",
        "am",
        "start",
        "-a",
        "android.intent.action.CALL",
        "-d",
        f"tel:{isd_code}{number}",
    ]
    result = subprocess.run(command, shell=False, capture_output=True, text=True)
    print("Successfully Called the Number {}".format(number))
    # Store the terminal response in variables
    terminal_error = result.stderr

    if terminal_error:
        return f"ADB error: {terminal_error.strip()}"
    return "Success"


if __name__ == "__main__":
    import android_device_connection_setup
    import time

    android_device_connection_setup.initialise()
    time.sleep(2)
    call("9999999999")
