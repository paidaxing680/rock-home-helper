import os
import time
import hashlib
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY")

URL = "https://wegame.shallow.ink/api/v1/games/rocom/ingame/home/info"

# =========================
# 🧠 V5缓存（内存版，可升级Redis）
# =========================
cache = {}        # uid -> {data, time}
ip_limit = {}     # ip -> time
uid_limit = {}    # uid -> time

CACHE_TTL = 60        # 缓存60秒（提升性能）
RATE_LIMIT = 8        # 8秒限制一次

SECRET = "v5_secret_key_888"


# =========================
# 🔐 签名验证
# =========================
def verify_sign(uid, ts, sign):
    raw = f"{uid}{ts}{SECRET}"
    expected = hashlib.md5(raw.encode()).hexdigest()
    return expected == sign


# =========================
# 🚀 主接口
# =========================
@app.route("/")
def query_home():

    uid = request.args.get("uid")
    ts = request.args.get("ts")
    sign = request.args.get("sign")

    ip = request.remote_addr

    if not uid:
        return jsonify({"success": False, "message": "缺少uid"})

    now = time.time()

    # =========================
    # ⛔ IP限流
    # =========================
    if ip in ip_limit and now - ip_limit[ip] < RATE_LIMIT:
        return jsonify({"success": False, "message": "IP请求过快"})

    ip_limit[ip] = now

    # =========================
    # ⛔ UID限流
    # =========================
    if uid in uid_limit and now - uid_limit[uid] < RATE_LIMIT:
        return jsonify({"success": False, "message": "UID请求过快"})

    uid_limit[uid] = now

    # =========================
    # ⚡ 缓存命中
    # =========================
    if uid in cache:
        data, t = cache[uid]["data"], cache[uid]["time"]
        if now - t < CACHE_TTL:
            return jsonify({
                "success": True,
                "source": "cache",
                "data": data
            })

    # =========================
    # 🔐 签名验证（可选）
    # =========================
    if ts and sign:
        if not verify_sign(uid, ts, sign):
            return jsonify({"success": False, "message": "签名错误"})

    if not API_KEY:
        return jsonify({"success": False, "message": "API_KEY未配置"})

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

        # =========================
        # ⚡ API请求（带重试）
        # =========================
        for i in range(2):
            try:
                response = requests.post(
                    URL,
                    headers=headers,
                    json=body,
                    timeout=12
                )
                result = response.json()

                if result.get("code") == 0:
                    break

            except:
                if i == 1:
                    return jsonify({
                        "success": False,
                        "message": "外部API失败"
                    })

        data = result.get("data", {})
        home_info = data.get("home_info", {})

        # =========================
        # 🧠 写入缓存
        # =========================
        cache[uid] = {
            "data": home_info,
            "time": now
        }

        return jsonify({
            "success": True,
            "source": "api",
            "data": home_info
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e)
        })
