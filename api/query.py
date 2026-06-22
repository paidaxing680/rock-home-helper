from http.server import BaseHTTPRequestHandler
import json
import requests
from datetime import datetime
import os

API_KEY = os.environ.get("API_KEY")

URL = "https://wegame.shallow.ink/api/v1/games/rocom/ingame/home/info"


class handler(BaseHTTPRequestHandler):

    def do_GET(self):

        try:

            from urllib.parse import urlparse, parse_qs

            query = parse_qs(
                urlparse(self.path).query
            )

            uid = int(query.get("uid", [0])[0])

            headers = {
                "X-API-Key": API_KEY,
                "Authorization": API_KEY,
                "Content-Type": "application/json"
            }

            body = {
                "uid": uid,
                "wait_ms": 5000
            }

            resp = requests.post(
                URL,
                headers=headers,
                json=body,
                timeout=15
            )

            data = resp.json()

            self.send_response(200)
            self.send_header(
                "Content-Type",
                "application/json"
            )
            self.end_headers()

            self.wfile.write(
                json.dumps(data).encode()
            )

        except Exception as e:

            self.send_response(500)
            self.send_header(
                "Content-Type",
                "application/json"
            )
            self.end_headers()

            self.wfile.write(
                json.dumps({
                    "error": str(e)
                }).encode()
            )
