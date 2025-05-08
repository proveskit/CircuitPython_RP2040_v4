import os
import platform
import shutil
import string

import requests

response = requests.get(
    "https://raw.githubusercontent.com/proveskit/flight_controller_board/main/Firmware/FC_FIRM_v4x_V2.uf2",
    timeout=30,
)
response.raise_for_status()

with open("firmware.uf2", "wb") as f:
    f.write(response.content)

user_os = platform.system()

if user_os == "Darwin":
    for directory in os.listdir("/Volumes/"):
        if directory == "RPI-RP2":
            shutil.move("firmware.uf2", "/Volumes/RPI-RP2")

elif user_os == "Windows":
    drives = []
    for letter in string.ascii_lowercase:
        if os.path.exists(f"{letter}:\\"):
            drives.append(f"{letter}:\\")

    for drive in drives:
        files = os.listdir(drive)
        if "INDEX.HTM" in files and "INFO_IF2.TXT" in files:
            # Found PROVES Kit bootloader directory
            shutil.move("firmware.uf2", drive)
