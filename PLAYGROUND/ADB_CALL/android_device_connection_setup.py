# ██████╗   ███████╗ ██╗    ██╗ ███████╗            ██████╗    ██████╗             ██████╗   ██████╗    ██████╗   ███████╗
# ██╔══██╗ ██╔════╝ ██║    ██║ ██╔════╝            ██╔══██╗ ██╔═══██╗         ██╔════╝ ██╔═══██╗ ██╔══██╗ ██╔════╝
# ██║    ██║ █████╗     ██║    ██║ ███████╗            ██║    ██║ ██║      ██║         ██║           ██║      ██║ ██║    ██║ █████╗  
# ██║    ██║ ██╔══╝    ╚██╗  ██╔╝ ╚════██║           ██║    ██║ ██║      ██║         ██║           ██║      ██║ ██║    ██║ ██╔══╝  
# ██████╔╝ ███████╗  ╚████╔╝  ███████║            ██████╔╝╚██████╔╝         ╚██████╗ ╚██████╔╝  ██████╔╝ ███████╗
# ╚═════╝  ╚══════╝    ╚═══╝     ╚══════╝            ╚═════╝    ╚═════╝             ╚═════╝   ╚═════╝    ╚═════╝   ╚══════╝


#  Made With 💓 By - Shreyas Pawar (AURA-AGI)
#  YouTube Channel: https://www.youtube.com/@AURA-Team

#  For any questions or concerns, reach out to us via our social media handles.
#  Our top choice for contact is Telegram: https://t.me/AURA-Team
#  You can also find us on other platforms listed above. We're here to help!

#  - YouTube Channel: https://www.youtube.com/@AURA-Team
#  - Telegram Group: https://t.me/AURA-Team
#  - Discord Server: https://discord.gg/ehwfVtsAts
#  - Instagram:
#    - Personal: https://www.instagram.com/Shreyas.shades_/
#    - Channel: https://www.instagram.com/AURA-Team_/

#  ------------------------------------------------------------------------------
#  Dive into the world of coding with AURA Team - where passion meets programming!
#  Make sure to hit that Subscribe button to stay tuned for exciting content!

#  Pro Tip: For optimal performance and a seamless experience, we recommend using
#  the default library versions demonstrated in this demo. Your coding journey just
#  got even better! Happy coding!
#  ----------------------------------------------------------------------------




import subprocess
import os
import time

def initialise():
    # Change directory to platform-tools
    platform_tools_directory = r"PLAYGROUND\ADB_CALL\platform-tools"
    os.chdir(platform_tools_directory)

    # Disconnecting previous connections...
    print("Establishing clean environment...")

    # Disconnect old connections
    subprocess.run(["adb.exe", "disconnect"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Configuring device connection...
    print("Configuring device connectivity...")

    # Setting up connected device
    subprocess.run(["adb.exe", "tcpip", "7070"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Waiting for device initialization...
    print("Waiting for device initialization...")

    # Waiting for device to initialize
    time.sleep(3)

    # Retrieving device IP address...
    print("Retrieving device IP address...")

    # Get device IP address
    ip_process = subprocess.Popen(["adb.exe", "shell", "ip", "addr", "show", "wlan0"], stdout=subprocess.PIPE)
    ip_output = subprocess.check_output(["find", "inet "], stdin=ip_process.stdout).decode("utf-8")
    ip_process.wait()
    ip_full_address = ip_output.split()[1]
    device_ip = ip_full_address.split("/")[0]
    print("Device IP address obtained:", device_ip)

    # Establishing connection to device...
    print("Initiating device connection...")

    # Connecting to device with obtained IP
    subprocess.run(["adb.exe", "connect", device_ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Set the IP address of your Android device
    target_device_ip = device_ip

    # Set the port number for ADB
    adb_port = "7070"

    # Set the path to the ADB executable
    adb_executable_path = "adb.exe"

    # Starting ADB server...
    print("Starting ADB server...")

    # Start the ADB server
    subprocess.run([adb_executable_path, "start-server"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Connecting to the Android device over Wi-Fi...
    print("Connecting to the Android device over Wi-Fi...")

    # Connect to the Android device over Wi-Fi
    subprocess.run([adb_executable_path, "connect", f"{target_device_ip}:{adb_port}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    print("Ready to Boost ................")
