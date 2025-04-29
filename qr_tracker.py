from flask import Flask, redirect
import json
import os

app = Flask(__name__)

DESTINATION_URL = "https://mason.gmu.edu/~skhan89/"
COUNTER_FILE = "scan_count.json"

def load_count():
    if not os.path.exists(COUNTER_FILE):
        return 0
    with open(COUNTER_FILE, "r") as f:
        return json.load(f).get("count", 0)

def save_count(count):
    with open(COUNTER_FILE, "w") as f:
        json.dump({"count": count}, f)

@app.route("/scan")
def track_and_redirect():
    count = load_count() + 1
    save_count(count)
    print(f"[INFO] QR code scanned {count} times.")
    return redirect(DESTINATION_URL)

@app.route("/")
def home():
    return f"QR Scan Count: {load_count()}"

if __name__ == "__main__":
    app.run(debug=True)
