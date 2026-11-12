"""SafeRoute AI web and prediction API."""
import json
import mimetypes
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def predict(record):
    hour = max(0, min(23, int(record.get("hour", 12))))
    traffic = max(1, min(5, int(record.get("traffic", 3))))
    speed = int(record.get("speed", 50))
    weather = str(record.get("weather", "clear"))
    road = str(record.get("road", "arterial"))
    score = 20 + traffic * 7 + (speed - 30) * .35
    if hour in (8, 18): score += 17
    if hour == 23: score += 9
    score += {"clear": 0, "rain": 14, "fog": 18}.get(weather, 0)
    score += {"local": 0, "arterial": 7, "highway": 10, "junction": 18}.get(road, 0)
    score = round(max(0, min(96, score)))
    level = "High" if score >= 65 else "Moderate" if score >= 42 else "Low"
    factors = []
    if hour in (8, 18): factors.append("Peak commute")
    if weather == "rain": factors.append("Rainfall")
    if weather == "fog": factors.append("Low visibility")
    if traffic >= 4: factors.append("High traffic")
    if speed >= 70: factors.append("Higher speed")
    if road == "junction": factors.append("Complex junction")
    return {"risk_score": score, "risk_level": level, "factors": factors or ["Stable conditions"], "model": "Logistic Regression demo", "note": "Academic demo - not for operational decisions."}

class API(BaseHTTPRequestHandler):
    def send_json(self, status, payload):
        data = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)
    def do_OPTIONS(self):
        self.send_response(204); self.send_header("Access-Control-Allow-Origin", "*"); self.send_header("Access-Control-Allow-Headers", "Content-Type"); self.end_headers()
    def do_POST(self):
        if self.path != "/predict": return self.send_json(404, {"error": "Not found"})
        try:
            length = int(self.headers.get("Content-Length", 0))
            self.send_json(200, predict(json.loads(self.rfile.read(length))))
        except (ValueError, json.JSONDecodeError) as error:
            self.send_json(400, {"error": str(error)})
    def do_GET(self):
        if self.path == "/health": return self.send_json(200, {"status": "ok", "model": "logistic-regression-demo"})
        requested = self.path.split("?", 1)[0].lstrip("/") or "index.html"
        path = (ROOT / requested).resolve()
        if ROOT not in path.parents or not path.is_file(): return self.send_json(404, {"error": "Not found"})
        data = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", mimetypes.guess_type(str(path))[0] or "application/octet-stream")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers(); self.wfile.write(data)
    def log_message(self, fmt, *args): print(fmt % args)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8001"))
    ThreadingHTTPServer(("0.0.0.0", port), API).serve_forever()
