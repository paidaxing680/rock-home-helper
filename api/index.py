from flask import Flask, request, jsonify
import requests
from datetime import datetime

app = Flask(**name**)

API_KEY = "你的API_KEY"

URL = "https://wegame.shallow.ink/api/v1/games/rocom/ingame/home/info"

@app.route("/")
def query_home():

```
uid = request.args.get("uid")

if not uid:
    return jsonify({
        "success": False,
        "message": "缺少uid参数"
    })

try:

    headers = {
        "X-API-Key": API_KEY,
        "Authorization": API_KEY,
        "Content-Type": "application/json"
    }

    body = {
        "uid": int(uid),
        "wait_ms": 5000
    }

    resp = requests.post(
        URL,
        headers=headers,
        json=body,
        timeout=15
    )

    res_data = resp.json()

    if res_data.get("code") != 0:
        return jsonify({
            "success": False,
            "message": res_data.get("message")
        })

    return jsonify({
        "success": True,
        "data": res_data.get("data", {})
    })

except Exception as e:
    return jsonify({
        "success": False,
        "message": str(e)
    })
```
