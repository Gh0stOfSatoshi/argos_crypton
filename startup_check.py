import os
import json
import subprocess
import sys

REQUIRED_FILES = [
    "argos_core.py",
    "argos_utils.py",
    "argos_config.json",
    "argos_daemon.py",
    "argos_alerts.py"
]

def check_files():
    print("🔍 Verifying required files...")
    missing = [f for f in REQUIRED_FILES if not os.path.isfile(f)]
    if missing:
        print(f"❌ Missing required files: {', '.join(missing)}")
        sys.exit(1)
    print("✅ All required files found.")

def check_config():
    print("🔍 Validating configuration file...")
    try:
        with open("argos_config.json") as f:
            config = json.load(f)
    except Exception as e:
        print(f"❌ Failed to read config: {e}")
        sys.exit(1)

    required_keys = ["coins", "interval_seconds"]
    for key in required_keys:
        if key not in config:
            print(f"❌ Missing key in config: {key}")
            sys.exit(1)

    if config.get("telegram_bot_token", "").startswith("REPLACE") or \
       config.get("telegram_chat_id", "").startswith("REPLACE"):
        if config.get("email_alerts") is not True:
            print("⚠️ Telegram alert credentials not set. Continuing without alerts.")
    print("✅ Config looks good.")

def launch_daemon():
    print("🚀 Launching daemon...")
    subprocess.run(["python3", "argos_daemon.py"])

if __name__ == "__main__":
    print("🛡️ Argos Startup Check")
    check_files()
    check_config()
    launch_daemon()
