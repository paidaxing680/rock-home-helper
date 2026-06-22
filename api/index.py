from flask import Flask, request, jsonify
import requests

app = Flask(**name**)

API_KEY = "sk-df7c33694b4a98280a038e311758b503"

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

    response = requests.post(
        URL,
        headers=headers,
        json=body,
        timeout=15
    )

    result = response.json()

    return jsonify(result)

except Exception as e:
    return jsonify({
        "success": False,
        "message": str(e)
    })
```
