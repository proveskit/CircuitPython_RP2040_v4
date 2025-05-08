import os
import platform
import shutil
import string

import requests

if not os.path.exists("firmware.uf2"):
    response = requests.get(
        "https://raw.githubusercontent.com/proveskit/flight_controller_board/main/Firmware/FC_FIRM_v4x_V2.uf2",
        timeout=30,
    )
    response.raise_for_status()

    with open("firmware.uf2", "wb") as f:
        f.write(response.content)

success = False
user_os = platform.system()

if user_os == "Darwin":
    for directory in os.listdir("/Volumes/"):
        if directory == "RPI-RP2":
            shutil.move("firmware.uf2", "/Volumes/RPI-RP2")
            success = True
            break

elif user_os == "Linux":
    # Check common mount points for Linux
    mount_points = ["/media", "/mnt"]
    for mount_point in mount_points:
        if os.path.exists(mount_point):
            for directory in os.listdir(mount_point):
                if directory == "RPI-RP2":
                    shutil.move("firmware.uf2", os.path.join(mount_point, "RPI-RP2"))
                    success = True
                    break

elif user_os == "Windows":
    drives = []
    for letter in string.ascii_lowercase:
        if os.path.exists(f"{letter}:\\"):
            drives.append(f"{letter}:\\")

    for drive in drives:
        files = os.listdir(drive)
        if "INDEX.HTM" in files and "INFO_UF2.TXT" in files:
            # Found PROVES Kit bootloader directory
            shutil.move("firmware.uf2", drive)
            success = True
            break

if not success:
    print("Failed to find PROVES Kit bootloader directory")
else:
    print("Firmware installed successfully")
