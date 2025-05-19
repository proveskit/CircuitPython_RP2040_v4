import os
import time

import storage

mount_points = [
    "/sd",
]

wait_time = 0.02

storage.disable_usb_drive()
print("Disabling USB drive")
time.sleep(wait_time)

storage.remount("/", False)
print("Remounting root filesystem")
time.sleep(wait_time)

attempts = 0
while attempts < 5:
    attempts += 1
    try:
        for path in mount_points:
            try:
                os.mkdir(path)
                print(f"Mount point {path} created.")
            except OSError:
                print(f"Mount point {path} already exists.")
    except Exception as e:
        print(f"Error creating mount point {path}: {e}")
        time.sleep(wait_time)
        continue

    break

storage.enable_usb_drive()
print("Enabling USB drive")
