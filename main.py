"""
陪伴玩偶后端 API (极简单向版)
手机发消息 -> 存 -> 玩偶定时拉取显示

启动: uvicorn main:app --host 0.0.0.0 --port 8000
"""
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import store

ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "pager2024")


class SendBody(BaseModel):
    text: str
    password: str = ""


app = FastAPI(title="Pager API")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/send")
def api_send(body: SendBody):
    """手机发消息给玩偶"""
    if body.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=403, detail="密码错误")
    if not body.text.strip():
        raise HTTPException(status_code=400, detail="内容为空")
    store.set_box_msg(body.text.strip())
    return {"ok": True}


@app.get("/api/inbox")
def api_inbox(device_id: str = "", since_id: int = 0):
    """玩偶拉取最新消息"""
    msg = store.get_box_msg()
    if msg and msg["id"] > since_id:
        return {"msg": msg}
    return {"msg": None}


# 手机网页 (静态, 放在所有 API 路由之后作为兜底)
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="static")
