import logging
from fastapi import FastAPI, Header, HTTPException
from app.config import get
from app.service import publish_once
logging.basicConfig(level=get("LOG_LEVEL","INFO"))
app=FastAPI(title="DIGO AI Social Manager")

@app.get("/health")
def health():
    return {"ok":True,"service":"DIGO AI Social Manager"}

@app.post("/run-now")
def run_now(x_admin_token: str=Header(default="")):
    if not get("ADMIN_TOKEN") or x_admin_token != get("ADMIN_TOKEN"):
        raise HTTPException(status_code=401,detail="Unauthorized")
    try: return publish_once()
    except Exception as exc:
        logging.exception("Manual publishing failed")
        raise HTTPException(status_code=500,detail=str(exc))
