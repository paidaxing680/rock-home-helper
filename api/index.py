import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# 🔐 安全：从环境变量读取
API_KEY = os.environ.get("API_KEY")

URL = "https://wegame.shallow.ink/api/v1/games/rocom/ingame/home/info"


@app.route("/")
def query_home():

    uid = request.args.get("uid")

    if not uid:
        return jsonify({
            "success": False,
            "message": "缺少uid参数"
        })

    # 🔐 防止未配置
    if not API_KEY:
        return jsonify({
            "success": False,
            "message": "服务器未配置API_KEY"
        }), 500

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

        if result.get("code") != 0:
            return jsonify(result)

        data = result.get("data", {})
        home_info = data.get("home_info", {})

        return jsonify({
            "success": True,
            "uid": uid,
            "home_info": home_info
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })
