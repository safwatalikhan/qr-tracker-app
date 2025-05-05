from flask import Flask, redirect, request, render_template_string
import json
import os
from datetime import datetime

app = Flask(__name__)

DESTINATION_URL = "https://docs.google.com/presentation/d/1tik_VISb33KO11ylgUTWy7coiovIRtDAWv7z1wpE730/edit?usp=sharing"
LOG_FILE = "scan_log.json"

def load_logs():
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r") as f:
        return json.load(f)

def save_logs(logs):
    with open(LOG_FILE, "w") as f:
        json.dump(logs, f, indent=2)

@app.route("/scan")
def track_and_redirect():
    logs = load_logs()
    new_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "ip": request.headers.get("X-Forwarded-For", request.remote_addr),
        "user_agent": request.headers.get("User-Agent")
    }
    logs.append(new_entry)
    save_logs(logs)
    return redirect(DESTINATION_URL)

@app.route("/")
def view_logs():
    logs = load_logs()
    total_scans = len(logs)
    return render_template_string("""
    <html>
    <head>
        <title>QR Scan Tracker</title>
        <style>
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; }
            th { background-color: #f2f2f2; }
        </style>
    </head>
    <body>
        <h2>Total Scans: {{ total }}</h2>
        <table>
            <tr>
                <th>#</th>
                <th>Timestamp (UTC)</th>
                <th>IP Address</th>
                <th>User Agent</th>
            </tr>
            {% for log in logs %}
            <tr>
                <td>{{ loop.index }}</td>
                <td>{{ log.timestamp }}</td>
                <td>{{ log.ip }}</td>
                <td>{{ log.user_agent }}</td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """, logs=logs, total=total_scans)
