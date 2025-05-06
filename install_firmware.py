import requests
import os
import shutil
import platform

response = requests.get(
    "https://raw.githubusercontent.com/proveskit/flight_controller_board/main/Firmware/FC_FIRM_v4x_V2.uf2")
response.raise_for_status()

with open("firmware.uf2", "wb") as f:
    f.write(response.content)

user_os = platform.system()
if user_os == "Darwin":
    for dir in os.listdir("/Volumes/"):
        if dir == "RPI-RP2":
            shutil.move("firmware.uf2", "/Volumes/RPI-RP2")
elif user_os == "Windows":
    for drive in os.listdrives():
        print(drive)