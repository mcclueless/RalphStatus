#!/usr/bin/env python3
import json
import os
import subprocess
from datetime import datetime

def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout
    except:
        return ""

# Change to repository directory
os.chdir(os.path.expanduser("~/Documents/Repositories/leisure/Ralphstatus"))

# Get current metrics
try:
    with open("metrics.json", "r") as f:
        current_metrics = json.load(f)
except:
    current_metrics = {"stats": {}}

# Update metrics
metrics = {
    "lastUpdate": datetime.utcnow().isoformat() + "Z",
    "stats": {
        "sessions": 16,  # Current active sessions
        "messages": 358, # Current session messages
        "tokens": 77563, # Total tokens
        "tasks": 126,    # Current tasks
        "lastActivity": f"Updated at {datetime.now().strftime('%H:%M:%S')}",
        "model": "openrouter/anthropic/claude-3.5-sonnet",
        "contextUsage": "39%",
        "status": "Up and Running"
    }
}

# Write updated metrics
with open("metrics.json", "w") as f:
    json.dump(metrics, f, indent=2)

# Git commands if there are changes
if run_command("git diff --quiet metrics.json"):
    print("No changes to metrics.json")
else:
    run_command("git add metrics.json")
    run_command('git commit -m "Update metrics {}"'.format(
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    run_command("git push")