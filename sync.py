"""
sync.py - automatically syncs parent source files to child projects.

Place this file in the `parent/` folder alongside main.py, validate.py, etc.
"""

import shutil
import time
import threading
from pathlib import Path

# ------------------------------
# CONFIG
# ------------------------------

# Parent source files
PARENT_FILES = ["main.py", "validate.py"]

# Child projects relative to parent folder
TARGET_PROJECTS = [
    "../PP_3_13",
    "../PP_3_14"
]

# Intervals (seconds)
INTERVAL_FAST = 2   # fast when changes detected
INTERVAL_SLOW = 30  # slow when idle

# ------------------------------
# FUNCTION: sync parent → child
# ------------------------------
def perform_sync():
    base_dir = Path(__file__).parent.resolve()  # parent folder
    parent_paths = [base_dir / f for f in PARENT_FILES]
    child_paths = [Path(p).resolve() for p in TARGET_PROJECTS]

    last_mtimes = {p.name: 0 for p in parent_paths}
    current_interval = INTERVAL_SLOW

    print("[SYNC] Background sync started...")

    while True:
        any_change = False
        for parent_path in parent_paths:
            if not parent_path.exists():
                continue
            current_mtime = parent_path.stat().st_mtime
            if current_mtime != last_mtimes[parent_path.name]:
                for child_dir in child_paths:
                    target_path = child_dir / parent_path.name
                    shutil.copy2(parent_path, target_path)
                    print(f"[SYNC] {parent_path} → {target_path}")
                last_mtimes[parent_path.name] = current_mtime
                any_change = True

        current_interval = INTERVAL_FAST if any_change else INTERVAL_SLOW
        time.sleep(current_interval)

# ------------------------------
# FUNCTION: start sync in background
# ------------------------------
def start_sync():
    thread = threading.Thread(target=perform_sync, daemon=True)
    thread.start()
    return thread

# ------------------------------
# MAIN
# ------------------------------
if __name__ == "__main__":
    print("[SYNC] Running sync.py directly. Press Ctrl+C to stop.")
    try:
        perform_sync()
    except KeyboardInterrupt:
        print("\n[SYNC] Sync stopped by user.")
